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

from xml.etree.ElementTree import Element

from intacctsdk.exceptions.intacct_exception import IntacctException


class Control:

    @property
    def status(self):
        return self._status

    @property
    def sender_id(self):
        return self._sender_id

    @property
    def control_id(self):
        return self._control_id

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def dtd_version(self):
        return self._dtd_version

    def __init__(self, control: Element):
        self._status = None
        self._sender_id = None
        self._control_id = None
        self._unique_id = None
        self._dtd_version = None

        status_element = control.find("status")
        if status_element is None:
            raise IntacctException("Control block is missing status element")
        sender_id_element = control.find("senderid")
        control_id_element = control.find("controlid")
        unique_id_element = control.find("uniqueid")
        dtd_version_element = control.find("dtdversion")

        if status_element is not None:
            self._status = status_element.text
        if sender_id_element is not None:
            self._sender_id = sender_id_element.text
        if control_id_element is not None:
            self._control_id = control_id_element.text
        if unique_id_element is not None:
            self._unique_id = unique_id_element.text
        if dtd_version_element is not None:
            self._dtd_version = dtd_version_element.text
