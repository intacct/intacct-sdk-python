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

from abc import ABC
from xml.etree import ElementTree

from intacctsdk.exceptions.intacct_exception import IntacctException
from intacctsdk.exceptions.response_exception import ResponseException
from intacctsdk.xmls.response.control import Control
from intacctsdk.xmls.response.error_message import ErrorMessage


class AbstractResponse(ABC):

    @property
    def xml(self):
        return self._xml

    @property
    def control(self):
        return self._control

    def __init__(self, body: str):
        self._xml = None
        self._control = None

        self._xml = ElementTree.fromstring(body)
        if self._xml.tag != 'response':
            raise IntacctException("Response XML is missing root response element")

        control_element = self._xml.find("control")
        if control_element is None:
            raise IntacctException("Response block is missing control element")

        self._control = Control(control_element)

        if self._control.status != "success":
            errors = []
            errormessage_element = self._xml.find("errormessage")
            if errormessage_element is not None:
                error_message = ErrorMessage(errormessage_element)
                errors = error_message.errors

            raise ResponseException("Response control status failure", errors)
