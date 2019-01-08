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

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.sender_credentials import SenderCredentials
from intacctsdk.credentials.session_credentials import SessionCredentials


class TestSessionCredentials(TestCase):

    def setUp(self):
        sender_config = ClientConfig()
        sender_config.sender_id = "testsenderid"
        sender_config.sender_password = "pass123!"
        self.senderCreds = SenderCredentials(sender_config)

    def testCredsFromConfig(self):
        config = ClientConfig()
        config.session_id = "faKEsesSiOnId.."
        config.endpoint_url = "https://p1.intacct.com/ia/xml/xmlgw.phtml"

        creds = SessionCredentials(config, self.senderCreds)
        self.assertEqual("faKEsesSiOnId..", creds.session_id)
        self.assertEqual("https://p1.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsFromConfigWithEmptyEndpoint(self):
        config = ClientConfig()
        config.session_id = "faKEsesSiOnId.."
        config.endpoint_url = None

        creds = SessionCredentials(config, self.senderCreds)
        self.assertEqual("faKEsesSiOnId..", creds.session_id)
        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testInvalidSessionIdException(self):
        config = ClientConfig()
        config.session_id = ""
        with self.assertRaises(Exception) as cm:
            creds = SessionCredentials(config, self.senderCreds)

        self.assertEqual('Required Session ID not supplied in config',
                         str(cm.exception))
