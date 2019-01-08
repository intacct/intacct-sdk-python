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


class ClientConfig:
    def __init__(self):
        from intacctsdk.credentials.login_credentials import LoginCredentials
        from intacctsdk.credentials.session_credentials import SessionCredentials

        self.profile_file: str = None
        self.profile_name: str = None
        self.endpoint_url: str = None
        self.sender_id: str = None
        self.sender_password: str = None
        self.session_id: str = None
        self.company_id: str = None
        self.entity_id: str = None
        self.user_id: str = None
        self.user_password: str = None
        self.credentials: LoginCredentials or SessionCredentials = None
        # self.logger: TODO = None
        # self.log_level: str = None
        # self.log_message_formatter: TODO = None
