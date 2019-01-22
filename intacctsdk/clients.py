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

import os
from abc import ABC
from typing import List

from .configs import ClientConfig, RequestConfig
from .credentials import SessionCredentials, LoginCredentials, SenderCredentials
from .functions import ApiFunctionInterface, ApiSessionCreate
from .handlers import RequestHandler
from .xml_responses import OnlineResponse, OfflineResponse


class AbstractClient(ABC):

    PROFILE_ENV_NAME = "INTACCT_PROFILE"

    def __init__(self, config: ClientConfig = None):
        self.config = None

        if config is None:
            config = ClientConfig()

        if config.profile_name is None:
            config.profile_name = os.getenv(self.PROFILE_ENV_NAME)

        if (
            isinstance(config.credentials, SessionCredentials)
            or isinstance(config.credentials, LoginCredentials)
        ):
            # Do not try and load credentials if they are already set in config
            pass
        elif config.session_id is not None:
            # Load the session credentials
            config.credentials = SessionCredentials(config, SenderCredentials(config))
        else:
            # Load the login credentials
            config.credentials = LoginCredentials(config, SenderCredentials(config))

        self.config = config

    def _execute_online_request(self, api_functions: List[ApiFunctionInterface], request_config: RequestConfig = None):
        if request_config is None:
            request_config = RequestConfig()

        request_handler = RequestHandler(self.config, request_config)

        return request_handler.execute_online(api_functions)

    def _execute_offline_request(self, api_functions: List[ApiFunctionInterface], request_config: RequestConfig = None):
        if request_config is None:
            request_config = RequestConfig()

        request_handler = RequestHandler(self.config, request_config)

        return request_handler.execute_offline(api_functions)


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


class OfflineClient(AbstractClient):

    def execute(self, api_function: ApiFunctionInterface,
                request_config: RequestConfig = None) -> OfflineResponse:
        if request_config is None:
            request_config = RequestConfig()

        api_functions = [
            api_function,
        ]

        response = self._execute_offline_request(api_functions, request_config)

        return response

    def execute_batch(self, api_functions: List[ApiFunctionInterface],
                      request_config: RequestConfig = None) -> OfflineResponse:
        if request_config is None:
            request_config = RequestConfig()

        response = self._execute_offline_request(api_functions, request_config)

        if request_config.transaction is True:
            for result in response.results:
                result.ensure_status_not_failure()

        return response


class SessionProvider:

    @staticmethod
    def factory(config: ClientConfig = None) -> ClientConfig:
        if config is None:
            config = ClientConfig()

        request_config = RequestConfig()
        request_config.control_id = "sessionProvider"
        request_config.no_retry_server_error_codes = []  # Retry all 500 level errors

        api_function = ApiSessionCreate()

        if config.session_id is not None and config.entity_id is not None:
            api_function.entity_id = config.entity_id

        client = OnlineClient(config)
        response = client.execute(api_function, request_config)

        authentication = response.authentication
        result = response.results[0]

        result.ensure_status_success()  # Throw any result errors

        data = result.data
        api = data[0]

        config.session_id = api.find("sessionid").text
        config.endpoint_url = api.find("endpoint").text
        config.entity_id = api.find("locationid").text

        config.company_id = authentication.company_id
        config.user_id = authentication.user_id

        config.credentials = SessionCredentials(config, SenderCredentials(config))

        return config
