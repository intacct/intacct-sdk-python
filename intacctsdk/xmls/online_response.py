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
from intacctsdk.exceptions.response_exception import ResponseException
from intacctsdk.xmls.abstract_response import AbstractResponse
from intacctsdk.xmls.response.result import Result
from intacctsdk.xmls.response.authentication import Authentication
from intacctsdk.xmls.response.error_message import ErrorMessage


class OnlineResponse(AbstractResponse):

    @property
    def authentication(self):
        return self._authentication

    @property
    def results(self):
        return self._results

    def __init__(self, body: str):
        self._authentication = None
        self._results = None

        super(OnlineResponse, self).__init__(body)

        self._results = []

        operation_element = self._xml.find("operation")
        if operation_element is None:
            raise IntacctException("Response block is missing operation block")

        auth_element = operation_element.find("authentication")
        if auth_element is None:
            raise IntacctException("Authentication block is missing from operation element")
        self._authentication = Authentication(auth_element)
        if self._authentication.status != "success":
            errormessage_element = operation_element.find("errormessage")
            errors = []
            if errormessage_element is not None:
                error_message = ErrorMessage(errormessage_element)
                errors = error_message.errors

            raise ResponseException("Response authentication status failure", errors)

        result_elements = operation_element.findall("result")
        if len(result_elements) < 1:
            raise IntacctException("Result block is missing from operation element")

        for result_element in result_elements:
            self._results.append(Result(result_element))

