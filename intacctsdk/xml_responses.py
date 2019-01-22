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

import re
from abc import ABC
from typing import List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .exceptions import IntacctException, ResponseException, ResultException


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


class ErrorMessage:

    @property
    def errors(self):
        return self._errors

    def __init__(self, error_messages: Element):
        self._errors = []

        error_contents = []
        for error_element in error_messages.findall("error"):
            pieces = ErrorMessage.combine_error_message_elements(error_element)
            error_contents.append(" ".join(pieces))

        self._errors = error_contents

    @staticmethod
    def combine_error_message_elements(error_element: Element):
        pieces = []
        for error_field in list(error_element):
            value = error_field.text
            if value is not None:
                piece = ErrorMessage.cleanse(value)
                pieces.append(piece)

        return pieces

    @staticmethod
    def cleanse(message: str) -> str:
        no_html = re.sub('<[^<]+?>', '', message)
        no_space = re.sub(' {2,}', ' ', no_html)

        return no_space


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


class Authentication:

    @property
    def status(self):
        return self._status

    @property
    def user_id(self):
        return self._user_id

    @property
    def company_id(self):
        return self._company_id

    @property
    def entity_id(self):
        return self._entity_id

    def __init__(self, auth: Element):
        self._status = None
        self._user_id = None
        self._company_id = None
        self._entity_id = None

        status_element = auth.find("status")
        if status_element is None:
            raise IntacctException("Authentication block is missing status element")
        user_id_element = auth.find("userid")
        if user_id_element is None:
            raise IntacctException("Authentication block is missing userid element")
        company_id_element = auth.find("companyid")
        if company_id_element is None:
            raise IntacctException("Authentication block is missing companyid element")
        entity_id_element = auth.find("locationid")

        self._status = status_element.text
        self._user_id = user_id_element.text
        self._company_id = company_id_element.text
        self._entity_id = entity_id_element.text

        # TODO add getter/setter for elements: clientstatus, clientid, sessiontimestamp


class Result:

    @property
    def status(self):
        return self._status

    @property
    def function_name(self):
        return self._function_name

    @property
    def control_id(self):
        return self._control_id

    @property
    def data(self) -> List[Element]:
        return self._data

    @property
    def list_type(self):
        return self._list_type

    @property
    def count(self):
        return self._count

    @property
    def total_count(self):
        return self._total_count

    @property
    def num_remaining(self):
        return self._num_remaining

    @property
    def result_id(self):
        return self._result_id

    @property
    def key(self):
        return self._key

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def errors(self):
        return self._errors

    def __init__(self, result: Element):
        self._status = None
        self._function_name = None
        self._control_id = None
        self._data = None
        self._list_type = None
        self._count = None
        self._total_count = None
        self._num_remaining = None
        self._result_id = None
        self._key = None
        self._start = None
        self._end = None
        self._errors = None

        status_element = result.find("status")
        if status_element is None:
            raise IntacctException("Response result block is missing status element")
        self._status = status_element.text
        function_element = result.find("function")
        if function_element is None:
            raise IntacctException("Response result block is missing function element")
        self._function_name = function_element.text
        control_id_element = result.find("controlid")
        if control_id_element is None:
            raise IntacctException("Response result block is missing controlid element")
        self._control_id = control_id_element.text

        if self._status != "success":
            error_message_element = result.find("errormessage")
            if error_message_element is not None:
                error_message = ErrorMessage(error_message_element)

                self._errors = error_message.errors
        else:
            key_element = result.find("key")
            list_type_element = result.find("listtype")
            data_element = result.find("data")

            if key_element is not None:
                self._key = key_element.text
            elif list_type_element is not None:
                self._list_type = list_type_element.text
                list_type_total_attr = list_type_element.get("total")
                if list_type_total_attr is not None:
                    self._total_count = int(list_type_total_attr)
                list_type_start_attr = list_type_element.get("start")
                if list_type_start_attr is not None:
                    self._start = int(list_type_start_attr)
                list_type_end_attr = list_type_element.get("end")
                if list_type_end_attr is not None:
                    self._end = int(list_type_end_attr)
            elif (
                data_element is not None
                and data_element.get("listtype") is not None
            ):
                data_list_type_attr = data_element.get("listtype")
                if data_list_type_attr is not None:
                    self._list_type = data_list_type_attr
                data_total_count_attr = data_element.get("totalcount")
                if data_total_count_attr is not None:
                    self._total_count = int(data_total_count_attr)
                data_count_attr = data_element.get("count")
                if data_count_attr is not None:
                    self._count = int(data_count_attr)
                data_num_remain_attr = data_element.get("numremaining")
                if data_num_remain_attr is not None:
                    self._num_remaining = int(data_num_remain_attr)
                data_result_id_attr = data_element.get("resultId")
                if data_result_id_attr is not None:
                    self._result_id = data_result_id_attr

            if data_element is not None:
                data = []
                for child in data_element:
                    data.append(child)

                self._data = data

    def ensure_status_success(self):
        if self.status != "success":
            raise ResultException("Result status: " + self.status + " for Control ID: " + self.control_id, self._errors)

    def ensure_status_not_failure(self):
        if self.status == "failure":
            raise ResultException("Result status: " + self.status + " for Control ID: " + self.control_id, self._errors)
