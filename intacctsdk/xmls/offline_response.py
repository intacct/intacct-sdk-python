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

from intacctsdk.exceptions.intacct_exception import IntacctException
from intacctsdk.xmls.abstract_response import AbstractResponse


class OfflineResponse(AbstractResponse):

    @property
    def status(self):
        return self._status

    def __init__(self, body: str):
        self._status = None

        super(OfflineResponse, self).__init__(body)

        acknowledgement_element = self._xml.find("acknowledgement")
        if acknowledgement_element is None:
            raise IntacctException("Response block is missing acknowledgement block")

        status_element = acknowledgement_element.find("status")
        if status_element is None:
            raise IntacctException("Acknowledgement block is missing status element")
        self._status = status_element.text
