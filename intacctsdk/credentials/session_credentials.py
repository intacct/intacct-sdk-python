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
from intacctsdk.credentials.endpoint import Endpoint
from intacctsdk.credentials.sender_credentials import SenderCredentials


class SessionCredentials:

    def __init__(self, config: ClientConfig, sender_creds: SenderCredentials):
        self.session_id: str = None
        self.endpoint: Endpoint = None
        self.sender_creds: SenderCredentials = None

        if config.session_id is None or config.session_id == "":
            raise Exception("Required Session ID not supplied in config")

        self.session_id = config.session_id

        if config.endpoint_url is not None:
            self.endpoint = Endpoint(config)
        else:
            self.endpoint = sender_creds.endpoint

        self.sender_creds = sender_creds
