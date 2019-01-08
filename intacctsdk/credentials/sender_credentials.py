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

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.endpoint import Endpoint
from intacctsdk.credentials.profile_credential_provider import ProfileCredentialProvider


class SenderCredentials:
    
    SENDER_PROFILE_ENV_NAME = "INTACCT_SENDER_PROFILE"

    SENDER_ID_ENV_NAME = "INTACCT_SENDER_ID"

    SENDER_PASSWORD_ENV_NAME = "INTACCT_SENDER_PASSWORD"

    DEFAULT_SENDER_PROFILE = "default"

    def __init__(self, config: ClientConfig):
        self.sender_id = None
        self.password = None
        self.endpoint = None

        env_profile_name = os.getenv(self.SENDER_PROFILE_ENV_NAME)
        if env_profile_name is None:
            env_profile_name = self.DEFAULT_SENDER_PROFILE
        if config.profile_name is None:
            config.profile_name = env_profile_name
        if config.sender_id is None:
            config.sender_id = os.getenv(self.SENDER_ID_ENV_NAME)
        if config.sender_password is None:
            config.sender_password = os.getenv(self.SENDER_PASSWORD_ENV_NAME)
        if (
                config.sender_id is None
                and config.sender_password is None
                and config.profile_name is not None
        ):
            profile = ProfileCredentialProvider.get_sender_credentials(config)

            if profile.sender_id is not None:
                config.sender_id = profile.sender_id
            if profile.sender_password is not None:
                config.sender_password = profile.sender_password
            if config.endpoint_url is None:
                # Only set the endpoint URL if it was never passed in to begin with
                config.endpoint_url = profile.endpoint_url

        if config.sender_id is None:
            raise Exception(
                'Required Sender ID not supplied in config or env variable "' + self.SENDER_ID_ENV_NAME + '"')
        if config.sender_password is None:
            raise Exception(
                'Required Sender Password not supplied in config or env variable "'
                + self.SENDER_PASSWORD_ENV_NAME + '"')

        self.sender_id = config.sender_id
        self.password = config.sender_password
        self.endpoint = Endpoint(config)
