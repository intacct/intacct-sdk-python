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
