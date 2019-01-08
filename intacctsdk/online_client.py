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

from intacctsdk.abstract_client import AbstractClient
from intacctsdk.functions.api_function import ApiFunctionInterface
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.online_response import OnlineResponse


class OnlineClient(AbstractClient):

    def execute(self, api_function: ApiFunctionInterface,
                request_config: RequestConfig = None) -> OnlineResponse:
        if request_config is None:
            request_config = RequestConfig()

        api_functions = [
            api_function,
        ]

        response = self._execute_online_request(api_functions, request_config)

        response.results[0].ensure_status_success()

        return response

    def execute_batch(self, api_functions: List[ApiFunctionInterface],
                      request_config: RequestConfig = None) -> OnlineResponse:
        if request_config is None:
            request_config = RequestConfig()

        response = self._execute_online_request(api_functions, request_config)

        if request_config.transaction is True:
            for result in response.results:
                result.ensure_status_not_failure()

        return response
