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
from typing import List

from intacctsdk.client_config import ClientConfig
from intacctsdk.functions.api_function import ApiFunctionInterface
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.request.control_block import ControlBlock
from intacctsdk.xmls.request.operation_block import OperationBlock


class RequestBlock:

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig, content: List[ApiFunctionInterface]):
        self._control_block = None
        self._operation_block = None
        self._encoding = None

        self._encoding = request_config.encoding
        self._control_block = ControlBlock(client_config, request_config)
        self._operation_block = OperationBlock(client_config, request_config, content)

    def write_xml(self) -> str:
        request = ElementTree.Element('request')

        self._control_block.write_xml(request)
        self._operation_block.write_xml(request)

        return ElementTree.tostring(request, encoding=self._encoding, method="xml")
