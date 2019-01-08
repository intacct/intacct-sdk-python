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
from intacctsdk.credentials.login_credentials import LoginCredentials
from intacctsdk.credentials.sender_credentials import SenderCredentials


class TestLoginCredentials(TestCase):

    def setUp(self):
        sender_config = ClientConfig()
        sender_config.sender_id = "testsenderid"
        sender_config.sender_password = "pass123!"
        self.senderCreds = SenderCredentials(sender_config)

    def testCredsFromConfig(self):
        config = ClientConfig()
        config.company_id = "testcompany"
        config.user_id = "testuser"
        config.user_password = "testpass"

        creds = LoginCredentials(config, self.senderCreds)
        self.assertEqual("testcompany", creds.company_id)
        self.assertIsNone(creds.entity_id)
        self.assertEqual("testuser", creds.user_id)
        self.assertEqual("testpass", creds.password)
        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsWithEntityIdFromConfig(self):
        config = ClientConfig()
        config.company_id = "testcompany"
        config.entity_id = "testentity"
        config.user_id = "testuser"
        config.user_password = "testpass"

        creds = LoginCredentials(config, self.senderCreds)
        self.assertEqual("testcompany", creds.company_id)
        self.assertEqual("testentity", creds.entity_id)
        self.assertEqual("testuser", creds.user_id)
        self.assertEqual("testpass", creds.password)
        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsFromEnv(self):
        with patch.dict('os.environ', {
            'INTACCT_COMPANY_ID': 'envcompany',
            'INTACCT_USER_ID': 'envuser',
            'INTACCT_USER_PASSWORD': 'envuserpass',
        }):
            config = ClientConfig()
            creds = LoginCredentials(config, self.senderCreds)
            self.assertEqual("envcompany", creds.company_id)
            self.assertIsNone(creds.entity_id)
            self.assertEqual("envuser", creds.user_id)
            self.assertEqual("envuserpass", creds.password)
            self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testCredsWithEntityIdFromEnv(self):
        with patch.dict('os.environ', {
            'INTACCT_COMPANY_ID': 'envcompany',
            'INTACCT_ENTITY_ID': 'enventity',
            'INTACCT_USER_ID': 'envuser',
            'INTACCT_USER_PASSWORD': 'envuserpass',
        }):
            config = ClientConfig()
            creds = LoginCredentials(config, self.senderCreds)
            self.assertEqual("envcompany", creds.company_id)
            self.assertEqual("enventity", creds.entity_id)
            self.assertEqual("envuser", creds.user_id)
            self.assertEqual("envuserpass", creds.password)
            self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", creds.endpoint.url)

    def testInvalidCompanyIdException(self):
        config = ClientConfig()
        # config.companyId = "testcompany"
        config.user_id = "testuser"
        config.user_password = "testpass"
        with self.assertRaises(Exception) as cm:
            creds = LoginCredentials(config, self.senderCreds)

        self.assertEqual('Required Company ID not supplied in config or env variable "INTACCT_COMPANY_ID"',
                         str(cm.exception))

    def testInvalidUserIdException(self):
        config = ClientConfig()
        config.company_id = "testcompany"
        # config.userId = "testuser"
        config.user_password = "testpass"
        with self.assertRaises(Exception) as cm:
            creds = LoginCredentials(config, self.senderCreds)

        self.assertEqual('Required User ID not supplied in config or env variable "INTACCT_USER_ID"', str(cm.exception))

    def testInvalidUserPasswordException(self):
        config = ClientConfig()
        config.company_id = "testcompany"
        config.user_id = "testuser"
        # config.user_password = "testpass"
        with self.assertRaises(Exception) as cm:
            creds = LoginCredentials(config, self.senderCreds)

        self.assertEqual('Required User Password not supplied in config or env variable "INTACCT_USER_PASSWORD"',
                         str(cm.exception))

    def testCredsFromIniProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        config.profile_name = "unittest"
        creds = LoginCredentials(config, self.senderCreds)

        self.assertEqual("inicompanyid", creds.company_id)
        self.assertIsNone(creds.entity_id)
        self.assertEqual("iniuserid", creds.user_id)
        self.assertEqual("iniuserpass", creds.password)

    def testCredsWithEntityFromIniProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        config.profile_name = "entity"
        creds = LoginCredentials(config, self.senderCreds)

        self.assertEqual("inicompanyid", creds.company_id)
        self.assertEqual("inientityid", creds.entity_id)
        self.assertEqual("iniuserid", creds.user_id)
        self.assertEqual("iniuserpass", creds.password)

