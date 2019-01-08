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

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.sender_credentials import SenderCredentials
from intacctsdk.credentials.session_credentials import SessionCredentials
from intacctsdk.functions.api_session import ApiSessionCreate
from intacctsdk.online_client import OnlineClient
from intacctsdk.request_config import RequestConfig


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
