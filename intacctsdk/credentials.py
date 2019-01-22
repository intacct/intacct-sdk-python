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

import configparser
import os
from urllib.parse import urlparse

from .configs import ClientConfig


class Endpoint:

    DEFAULT_ENDPOINT = "https://api.intacct.com/ia/xml/xmlgw.phtml"

    ENDPOINT_URL_ENV_NAME = "INTACCT_ENDPOINT_URL"

    DOMAIN_NAME = "intacct.com"

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if value is None or value == "":
            value = self.DEFAULT_ENDPOINT

        test = urlparse(value)
        check = "." + self.DOMAIN_NAME
        if test.hostname[-len(check):] != check:
            raise Exception("Endpoint URL is not a valid " + self.DOMAIN_NAME + " domain name.")

        self._url = value

    def __init__(self, config: ClientConfig):
        if config.endpoint_url is None:
            self.url = os.getenv(self.ENDPOINT_URL_ENV_NAME)
        else:
            self.url = config.endpoint_url


class ProfileCredentialProvider:

    DEFAULT_PROFILE_FILE = os.path.join(".intacct", "credentials.ini")

    DEFAULT_PROFILE_NAME = "default"

    @staticmethod
    def get_login_credentials(config: ClientConfig):
        creds = ClientConfig()
        data = ProfileCredentialProvider.get_ini_profile_data(config)

        if "company_id" in data:
            creds.company_id = data["company_id"]
        if "entity_id" in data:
            creds.entity_id = data["entity_id"]
        if "user_id" in data:
            creds.user_id = data["user_id"]
        if "user_password" in data:
            creds.user_password = data["user_password"]

        return creds

    @staticmethod
    def get_sender_credentials(config: ClientConfig):
        creds = ClientConfig()
        data = ProfileCredentialProvider.get_ini_profile_data(config)

        if "sender_id" in data:
            creds.sender_id = data["sender_id"]
        if "sender_password" in data:
            creds.sender_password = data["sender_password"]
        if "endpoint_url" in data:
            creds.endpoint_url = data["endpoint_url"]

        return creds

    @staticmethod
    def get_home_dir_profile():
        profile = ""
        home_dir = os.getenv("HOME")

        if home_dir:
            # Linux/Unix
            profile = os.path.join(home_dir, ProfileCredentialProvider.DEFAULT_PROFILE_FILE)
        else:
            # Windows
            home_drive = os.getenv("HOMEDRIVE")
            home_path = os.getenv("HOMEPATH")
            if home_drive and home_path:
                profile = os.path.join(home_drive, home_path, ProfileCredentialProvider.DEFAULT_PROFILE_FILE)

        return profile

    @staticmethod
    def get_ini_profile_data(config: ClientConfig):
        if config.profile_name is None:
            config.profile_name = ProfileCredentialProvider.DEFAULT_PROFILE_NAME
        if config.profile_file is None:
            config.profile_file = ProfileCredentialProvider.get_home_dir_profile()

        # https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
        # `key="value"` will be loaded with the quotation marks therefore you must use `key=value` instead
        data = configparser.ConfigParser()
        data.read(config.profile_file)

        if config.profile_name not in data:
            raise Exception('Profile Name "' + config.profile_name + '" not found in credentials file')

        return data[config.profile_name]


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
        self.company_id = None
        self.entity_id = None
        self.user_id = None
        self.password = None
        self.sender_creds = None

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


class SessionCredentials:

    def __init__(self, config: ClientConfig, sender_creds: SenderCredentials):
        self.session_id = None
        self.endpoint = None
        self.sender_creds = None

        if config.session_id is None or config.session_id == "":
            raise Exception("Required Session ID not supplied in config")

        self.session_id = config.session_id

        if config.endpoint_url is not None:
            self.endpoint = Endpoint(config)
        else:
            self.endpoint = sender_creds.endpoint

        self.sender_creds = sender_creds
