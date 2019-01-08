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
