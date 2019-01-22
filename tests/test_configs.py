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

from unittest import TestCase

from intacctsdk.configs import ClientConfig, RequestConfig


class TestClientConfig(TestCase):

    def testDefaults(self):
        config = ClientConfig()

        self.assertIsNone(config.profile_file)
        self.assertIsNone(config.profile_name)
        self.assertIsNone(config.endpoint_url)
        self.assertIsNone(config.sender_password)
        self.assertIsNone(config.sender_password)
        self.assertIsNone(config.session_id)
        self.assertIsNone(config.company_id)
        self.assertIsNone(config.entity_id)
        self.assertIsNone(config.user_id)
        self.assertIsNone(config.user_password)
        self.assertIsNone(config.credentials)
        # TODO self.assertIsNone(config.logger)
        # TODO self.assertIsNone(config.logLevel)
        # TODO self.assertIsNone(config.logMessageFormatter)


class TestRequestConfig(TestCase):

    def testDefaults(self):
        config = RequestConfig()
        config.control_id = "unittest"

        self.assertEqual("unittest", config.control_id)
        self.assertEqual("UTF-8", config.encoding)
        self.assertEqual(5, config.max_retries)
        self.assertEqual(300, config.max_timeout)
        self.assertEqual([524], config.no_retry_server_error_codes)
        self.assertEqual("", config.policy_id)
        self.assertFalse(config.transaction)
        self.assertFalse(config.unique_id)
