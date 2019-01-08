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
        self.profile_file = None
        self.profile_name = None
        self.endpoint_url = None
        self.sender_id = None
        self.sender_password = None
        self.session_id = None
        self.company_id = None
        self.entity_id = None
        self.user_id = None
        self.user_password = None
        self.credentials = None
        # self.logger: TODO = None
        # self.log_level = None
        # self.log_message_formatter: TODO = None
