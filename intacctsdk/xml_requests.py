#  Copyright 2019 Sage Intacct, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"). You may not
#  use this file except in compliance with the License. You may obtain a copy
#  of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "LICENSE" file accompanying this file. This file is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.

import time
from typing import List
from xml.etree import ElementTree

from .configs import ClientConfig, RequestConfig
from .credentials import SessionCredentials, LoginCredentials
from .functions import ApiFunctionInterface


class RequestBlock:

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig, content: List[ApiFunctionInterface]):
        self._control_block = None
        self._operation_block = None
        self._encoding = None

        self._encoding = request_config.encoding
        self._control_block = ControlBlock(client_config, request_config)
        self._operation_block = OperationBlock(client_config, request_config, content)

    def write_xml(self) -> str:
        request = ElementTree.Element('request')

        self._control_block.write_xml(request)
        self._operation_block.write_xml(request)

        return ElementTree.tostring(request, encoding=self._encoding, method="xml")


class ControlBlock:

    @property
    def sender_id(self):
        return self._sender_id

    @sender_id.setter
    def sender_id(self, value: str):
        if value is None or value == "":
            raise Exception("Sender ID is required and cannot be blank")
        self._sender_id = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        if value is None or value == "":
            raise Exception("Sender Password is required and cannot be blank")
        self._password = value

    @property
    def control_id(self):
        return self._control_id

    @control_id.setter
    def control_id(self, value: str):
        if value is None or value == "":
            value = time.time().__str__()
        if len(value) < 1 or len(value) > 256:
            raise Exception("Request control ID must be between 1 and 256 characters in length.")
        self._control_id = value

    @property
    def unique_id(self):
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value: bool):
        self._unique_id = value

    @property
    def dtd_version(self):
        return self._dtd_version

    @property
    def policy_id(self):
        return self._policy_id

    @policy_id.setter
    def policy_id(self, value: str):
        self._policy_id = value

    @property
    def include_whitespace(self):
        return self._include_whitespace

    @include_whitespace.setter
    def include_whitespace(self, value: bool):
        self._include_whitespace = value

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig):
        self.sender_id = client_config.sender_id
        self.password = client_config.sender_password
        self.control_id = request_config.control_id
        self.unique_id = request_config.unique_id
        self.policy_id = request_config.policy_id
        self.include_whitespace = False
        self._dtd_version = "3.0"

    def write_xml(self, request: ElementTree) -> ElementTree:
        control = ElementTree.SubElement(request, "control")
        ElementTree.SubElement(control, "senderid").text = self.sender_id
        ElementTree.SubElement(control, "password").text = self.password
        ElementTree.SubElement(control, "controlid").text = self.control_id
        ElementTree.SubElement(control, "uniqueid").text = "true" if self.unique_id is True else "false"
        ElementTree.SubElement(control, "dtdversion").text = self.dtd_version
        if self.policy_id is not None and self.policy_id != "":
            ElementTree.SubElement(control, "policyid").text = self.policy_id
        ElementTree.SubElement(control,
                               "includewhitespace").text = "true" if self.include_whitespace is True else "false"


class OperationBlock:

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig, content: List[ApiFunctionInterface]):
        self.transaction = None
        self.authentication = None
        self.content = None

        self.transaction = request_config.transaction

        credentials = client_config.credentials
        if credentials is not None and isinstance(credentials, SessionCredentials):
            self.authentication = SessionAuthentication(credentials.session_id)
        elif credentials is not None and isinstance(credentials, LoginCredentials):
            self.authentication = LoginAuthentication(
                credentials.user_id, credentials.company_id, credentials.password, credentials.entity_id)
        elif client_config.session_id is not None:
            self.authentication = SessionAuthentication(client_config.session_id)
        elif (
                client_config.company_id is not None
                and client_config.user_id is not None
                and client_config.user_password is not None
        ):
            self.authentication = LoginAuthentication(
                client_config.user_id, client_config.company_id, client_config.user_password, client_config.entity_id)
        else:
            raise Exception("Authentication credentials [Company ID, User ID, and User Password] or [Session ID] " +
                            "are required and cannot be blank.")

        self.content = content

    def write_xml(self, request: ElementTree) -> ElementTree:
        operation = ElementTree.SubElement(request, "operation")
        operation.set("transaction", "true" if self.transaction is True else "false")

        self.authentication.write_xml(operation)

        content = ElementTree.SubElement(operation, "content")
        for api_function in self.content:
            api_function.write_xml(content)


class LoginAuthentication:

    @property
    def company_id(self):
        return self._company_id

    @company_id.setter
    def company_id(self, value: str):
        if value is None or value == "":
            raise Exception("Company ID is required and cannot be blank")
        self._company_id = value

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value: str):
        self._entity_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value: str):
        if value is None or value == "":
            raise Exception("User ID is required and cannot be blank")
        self._user_id = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        if value is None or value == "":
            raise Exception("User Password is required and cannot be blank")
        self._password = value

    def __init__(self, user_id: str, company_id: str, user_password: str, entity_id: str = None):
        self.company_id = company_id
        self.user_id = user_id
        self.password = user_password
        self.entity_id = entity_id

    def write_xml(self, operation: ElementTree) -> ElementTree:
        authentication = ElementTree.SubElement(operation, "authentication")
        login = ElementTree.SubElement(authentication, "login")
        ElementTree.SubElement(login, "userid").text = self.user_id
        ElementTree.SubElement(login, "companyid").text = self.company_id
        ElementTree.SubElement(login, "password").text = self.password
        if self.entity_id is not None:
            ElementTree.SubElement(login, "locationid").text = self.entity_id


class SessionAuthentication:

    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, value: str):
        if value is None or value == "":
            raise Exception("Session ID is required and cannot be blank")
        self._session_id = value

    def __init__(self, session_id: str):
        self.session_id = session_id

    def write_xml(self, operation: ElementTree) -> ElementTree:
        authentication = ElementTree.SubElement(operation, "authentication")
        ElementTree.SubElement(authentication, "sessionid").text = self.session_id
