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

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.profile_credential_provider import ProfileCredentialProvider


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
