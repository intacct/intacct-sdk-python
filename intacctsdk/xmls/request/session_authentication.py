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
