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

from intacctsdk.client_config import ClientConfig


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

        data = configparser.ConfigParser()
        data.read(config.profile_file)

        if config.profile_name not in data:
            raise Exception('Profile Name "' + config.profile_name + '" not found in credentials file')

        return data[config.profile_name]
