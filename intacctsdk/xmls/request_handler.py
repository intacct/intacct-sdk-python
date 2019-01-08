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

import time
import math
import requests
from typing import List

from requests import HTTPError

from intacctsdk.version import __version__
from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.endpoint import Endpoint
from intacctsdk.functions.api_function import ApiFunctionInterface
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.offline_response import OfflineResponse
from intacctsdk.xmls.online_response import OnlineResponse
from intacctsdk.xmls.request_block import RequestBlock


class RequestHandler:

    def __init__(self, client_config: ClientConfig, request_config: RequestConfig):
        self._version = __version__
        self.client_config = None
        self.request_config = None
        self.endpoint_url = None

        if client_config.endpoint_url is not None and client_config.endpoint_url != "":
            self.endpoint_url = client_config.endpoint_url
        else:
            endpoint = Endpoint(client_config)
            self.endpoint_url = endpoint.url

        self.client_config = client_config
        self.request_config = request_config

    def execute_online(self, content: List[ApiFunctionInterface]):
        if self.request_config.policy_id is not None and self.request_config.policy_id != "":
            self.request_config.policy_id = None

        request = RequestBlock(self.client_config, self.request_config, content)
        response = self.execute(request.write_xml())

        return OnlineResponse(response.content)

    def execute_offline(self, content: List[ApiFunctionInterface]):
        if self.request_config.policy_id is None or self.request_config.policy_id == "":
            raise Exception("Required Policy ID not supplied in config for offline request")

        # TODO logger warning section for session creds in offline request

        request = RequestBlock(self.client_config, self.request_config, content)
        response = self.execute(request.write_xml())

        return OfflineResponse(response.content)

    def execute(self, xml: str):
        headers = {
            'Content-Type': 'application/xml; encoding:' + self.request_config.encoding,
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'User-Agent': 'intacct-sdk-python-client/' + self._version,
        }

        attempt = 0
        while attempt <= self.request_config.max_retries:
            if attempt > 0:
                # Delay this retry based on exponential delay
                self.exponential_delay(attempt)
            try:
                response = requests.post(self.endpoint_url, data=xml, headers=headers,
                                         timeout=self.request_config.max_timeout)
                response.raise_for_status()
                return response

            except HTTPError as error:
                if 500 <= error.response.status_code <= 599:
                    if error.response.status_code in self.request_config.no_retry_server_error_codes:
                        raise error
                    elif attempt < self.request_config.max_retries:
                        attempt += 1
                    else:
                        raise error
                else:
                    raise error
        raise Exception("Request retry count exceeded max retry count: " + str(self.request_config.max_retries))

    @staticmethod
    def exponential_delay(retries: int):
        delay = math.pow(2, retries - 1)
        time.sleep(delay)
