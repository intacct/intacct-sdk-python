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
from unittest import TestCase
from unittest.mock import patch

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.sender_credentials import SenderCredentials


class TestSenderCredentials(TestCase):

    def testCredsFromConfig(self):
        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.endpoint_url = "https://unittest.intacct.com/ia/xml/xmlgw.phtml"

        creds = SenderCredentials(config)
        self.assertEqual("testsenderid", creds.sender_id)
        self.assertEqual("pass123!", creds.password)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsFromEnv(self):
        with patch.dict('os.environ', {
            'INTACCT_SENDER_ID': 'envsender',
            'INTACCT_SENDER_PASSWORD': 'envpass',
        }):
            config = ClientConfig()
            creds = SenderCredentials(config)
            self.assertEqual("envsender", creds.sender_id)
            self.assertEqual("envpass", creds.password)
            self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testInvalidSenderIdException(self):
        config = ClientConfig()
        # config.senderId = "testsenderid"
        config.sender_password = "pass123!"
        with self.assertRaises(Exception) as cm:
            creds = SenderCredentials(config)

        self.assertEqual('Required Sender ID not supplied in config or env variable "INTACCT_SENDER_ID"',
                         str(cm.exception))

    def testInvalidSenderPasswordException(self):
        config = ClientConfig()
        config.sender_id = "testsenderid"
        # config.sender_password = "pass123!"
        with self.assertRaises(Exception) as cm:
            creds = SenderCredentials(config)

        self.assertEqual('Required Sender Password not supplied in config or env variable "INTACCT_SENDER_PASSWORD"',
                         str(cm.exception))

    def testCredsFromIniProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        # use default profile name
        creds = SenderCredentials(config)

        self.assertEqual("defsenderid", creds.sender_id)
        self.assertEqual("defsenderpass", creds.password)
        self.assertEqual("https://default.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsFromIniProfileWithEndpointOverride(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        config.profile_name = "anothertest"
        creds = SenderCredentials(config)

        self.assertEqual("inisenderid", creds.sender_id)
        self.assertEqual("inisenderpass", creds.password)
        self.assertEqual("https://somethingelse.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

