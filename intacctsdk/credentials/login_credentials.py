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
from intacctsdk.credentials.profile_credential_provider import ProfileCredentialProvider
from intacctsdk.credentials.sender_credentials import SenderCredentials


class LoginCredentials:

    COMPANY_PROFILE_ENV_NAME = "INTACCT_COMPANY_PROFILE"

    COMPANY_ID_ENV_NAME = "INTACCT_COMPANY_ID"

    ENTITY_ID_ENV_NAME = "INTACCT_ENTITY_ID"

    USER_ID_ENV_NAME = "INTACCT_USER_ID"

    USER_PASSWORD_ENV_NAME = "INTACCT_USER_PASSWORD"

    DEFAULT_COMPANY_PROFILE = "default"

    @property
    def endpoint(self):
        return self.sender_creds.endpoint

    def __init__(self, config: ClientConfig, sender_creds: SenderCredentials):
        self.company_id: str = None
        self.entity_id: str = None
        self.user_id: str = None
        self.password: str = None
        self.sender_creds: SenderCredentials = None

        env_profile_name = os.getenv(self.COMPANY_PROFILE_ENV_NAME)
        if env_profile_name is None:
            env_profile_name = self.DEFAULT_COMPANY_PROFILE
        if config.profile_name is None:
            config.profile_name = env_profile_name
        if config.company_id is None:
            config.company_id = os.getenv(self.COMPANY_ID_ENV_NAME)
        if config.entity_id is None:
            config.entity_id = os.getenv(self.ENTITY_ID_ENV_NAME)
        if config.user_id is None:
            config.user_id = os.getenv(self.USER_ID_ENV_NAME)
        if config.user_password is None:
            config.user_password = os.getenv(self.USER_PASSWORD_ENV_NAME)
        if (
            config.company_id is None
            and config.user_id is None
            and config.user_password is None
            and config.profile_name is not None
        ):
            profile = ProfileCredentialProvider.get_login_credentials(config)

            if profile.company_id is not None:
                config.company_id = profile.company_id
            if profile.entity_id is not None:
                config.entity_id = profile.entity_id
            if profile.user_id is not None:
                config.user_id = profile.user_id
            if profile.user_password is not None:
                config.user_password = profile.user_password

        if config.company_id is None:
            raise Exception(
                'Required Company ID not supplied in config or env variable "' + self.COMPANY_ID_ENV_NAME + '"')
        # Entity ID is not required, no Exception
        if config.user_id is None:
            raise Exception(
                'Required User ID not supplied in config or env variable "' + self.USER_ID_ENV_NAME + '"')
        if config.user_password is None:
            raise Exception(
                'Required User Password not supplied in config or env variable "' + self.USER_PASSWORD_ENV_NAME + '"')

        self.company_id = config.company_id
        self.entity_id = config.entity_id
        self.user_id = config.user_id
        self.password = config.user_password
        self.sender_creds = sender_creds
