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


from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.login_credentials import LoginCredentials
from intacctsdk.credentials.sender_credentials import SenderCredentials
from intacctsdk.credentials.session_credentials import SessionCredentials
from intacctsdk.functions.api_function import ApiFunctionInterface
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.request_handler import RequestHandler


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
