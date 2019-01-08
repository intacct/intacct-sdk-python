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

import uuid
from abc import ABC, abstractmethod
from xml.etree import ElementTree


class ApiFunctionInterface(ABC):

    def __init__(self):
        self.control_id = None

    @abstractmethod
    def write_xml(self, xml: ElementTree) -> ElementTree:
        pass


class AbstractApiFunction(ApiFunctionInterface):

    @property
    def control_id(self):
        return self._control_id

    @control_id.setter
    def control_id(self, value: str):
        if value is None or value == "":
            value = str(uuid.uuid4())
        if len(value) < 1 or len(value) > 256:
            raise Exception("Function control ID must be between 1 and 256 characters in length.")
        self._control_id = value

    def __init__(self, control_id: str = None):
        self._control_id = None

        super(AbstractApiFunction, self).__init__()

        self.control_id = control_id

    @abstractmethod
    def write_xml(self, xml: ElementTree) -> ElementTree:
        pass
