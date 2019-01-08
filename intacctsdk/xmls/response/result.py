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

from typing import List
from xml.etree.ElementTree import Element

from intacctsdk.exceptions.intacct_exception import IntacctException
from intacctsdk.exceptions.result_exception import ResultException
from intacctsdk.xmls.response.error_message import ErrorMessage


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
