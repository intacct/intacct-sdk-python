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

from intacctsdk.functions.api_function import AbstractApiFunction


class ApiSessionCreate(AbstractApiFunction):

    def __init__(self, control_id: str = None):
        super(ApiSessionCreate, self).__init__(control_id)

        self.entity_id = None

    def write_xml(self, xml: ElementTree) -> ElementTree:
        api_function = ElementTree.SubElement(xml, "function")
        api_function.set("controlid", self.control_id)

        session = ElementTree.SubElement(api_function, "getAPISession")

        if self.entity_id is not None:
            ElementTree.SubElement(session, "locationid").text = self.entity_id
