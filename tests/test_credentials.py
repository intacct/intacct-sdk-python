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

from intacctsdk.configs import ClientConfig
from intacctsdk.credentials import Endpoint, ProfileCredentialProvider, SenderCredentials, LoginCredentials, SessionCredentials


class TestEndpoint(TestCase):

    def testDefaultEndpoint(self):
        config = ClientConfig()
        endpoint = Endpoint(config)

        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testEnvEndpoint(self):
        with patch.dict('os.environ', {'INTACCT_ENDPOINT_URL': 'https://envunittest.intacct.com/ia/xml/xmlgw.phtml'}):
            config = ClientConfig()
            endpoint = Endpoint(config)

            self.assertEqual("https://envunittest.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testConfigEndpoint(self):
        config = ClientConfig()
        config.endpoint_url = "https://configtest.intacct.com/ia/xml/xmlgw.phtml"
        endpoint = Endpoint(config)

        self.assertEqual("https://configtest.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testDefaultEndpointIfConfigIsNull(self):
        config = ClientConfig()
        config.endpoint_url = ""
        endpoint = Endpoint(config)

        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testInvalidEndpointException(self):
        config = ClientConfig()
        config.endpoint_url = "https://www.example.com/xmlgw.phtml"
        with self.assertRaises(Exception) as cm:
            endpoint = Endpoint(config)

        self.assertEqual("Endpoint URL is not a valid intacct.com domain name.", str(cm.exception))


class TestProfileCredentialProvider(TestCase):

    def testCredsFromIniDefaultProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        login_creds = ProfileCredentialProvider.get_login_credentials(config)

        self.assertEqual("defcompanyid", login_creds.company_id)
        self.assertIsNone(login_creds.entity_id)
        self.assertEqual("defuserid", login_creds.user_id)
        self.assertEqual("defuserpass", login_creds.user_password)

        sender_creds = ProfileCredentialProvider.get_sender_credentials(config)

        self.assertEqual("defsenderid", sender_creds.sender_id)
        self.assertEqual("defsenderpass", sender_creds.sender_password)
        self.assertEqual("https://default.intacct.com/ia/xml/xmlgw.phtml", sender_creds.endpoint_url)

    def testCredsFromIniSpecificProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        config.profile_name = "unittest"
        login_creds = ProfileCredentialProvider.get_login_credentials(config)

        self.assertEqual("inicompanyid", login_creds.company_id)
        self.assertIsNone(login_creds.entity_id)
        self.assertEqual("iniuserid", login_creds.user_id)
        self.assertEqual("iniuserpass", login_creds.user_password)

    def testCredsWithEntityFromIniSpecificProfile(self):
        config = ClientConfig()
        config.profile_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.ini')
        config.profile_name = "entity"
        login_creds = ProfileCredentialProvider.get_login_credentials(config)

        self.assertEqual("inicompanyid", login_creds.company_id)
        self.assertEqual("inientityid", login_creds.entity_id)
        self.assertEqual("iniuserid", login_creds.user_id)
        self.assertEqual("iniuserpass", login_creds.user_password)

    def testInvalidProfileNameException(self):
        config = ClientConfig()
        config.profile_name = "wrongname"
        with self.assertRaises(Exception) as cm:
            login_creds = ProfileCredentialProvider.get_login_credentials(config)

        self.assertEqual('Profile Name "wrongname" not found in credentials file', str(cm.exception))


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
