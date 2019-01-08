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
from xml.etree import ElementTree

from intacctsdk.client_config import ClientConfig
from intacctsdk.request_config import RequestConfig


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
