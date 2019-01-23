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

from logging import DEBUG
import time

from .logs import MessageFormatter


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
        self.log_level = DEBUG
        self.log_message_formatter = MessageFormatter()


class RequestConfig:

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value: int):
        if value < 0:
            raise Exception("Max Retries must be zero or greater")
        self._max_retries = value

    @property
    def max_timeout(self):
        return self._max_timeout

    @max_timeout.setter
    def max_timeout(self, value: int):
        if value < 0:
            raise Exception("Max Timeout must be zero or greater")
        self._max_timeout = value

    @property
    def no_retry_server_error_codes(self):
        return self._no_retry_server_error_codes

    @no_retry_server_error_codes.setter
    def no_retry_server_error_codes(self, value: []):
        for error_code in value:
            if error_code < 500 or error_code > 599:
                raise Exception("No Retry Server Error Codes must be between 500-599")
        self._no_retry_server_error_codes = value

    def __init__(self):
        self.control_id = time.time().__str__()
        self.encoding = "UTF-8"
        self.max_retries = 5
        self.max_timeout = 300
        self.no_retry_server_error_codes = [524]
        self.policy_id = ""
        self.transaction = False
        self.unique_id = False
