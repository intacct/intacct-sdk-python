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

from xml.etree import ElementTree
from typing import List

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.login_credentials import LoginCredentials
from intacctsdk.credentials.session_credentials import SessionCredentials
from intacctsdk.functions.api_function import ApiFunctionInterface
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.request.login_authentication import LoginAuthentication
from intacctsdk.xmls.request.session_authentication import SessionAuthentication


class OperationBlock:

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig, content: List[ApiFunctionInterface]):
        self.transaction: bool = None
        self.authentication: LoginCredentials or SessionCredentials = None
        self.content: [] = None

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
