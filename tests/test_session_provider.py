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

import responses
from unittest import TestCase
from unittest.mock import patch

from intacctsdk.client_config import ClientConfig
from intacctsdk.session_provider import SessionProvider


class TestSessionProvider(TestCase):

    @responses.activate
    def testFromLoginCredentials(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid></locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.company_id = "testcompany"
        config.user_id = "testuser"
        config.user_password = "testpass"

        session_creds = SessionProvider.factory(config)
        self.assertEqual("fAkESesSiOnId..", session_creds.session_id)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
        self.assertIsNone(session_creds.entity_id)

    @responses.activate
    def testFromLoginCredentialsWithEntity(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid>testentity</locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid>testentity</locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.company_id = "testcompany"
        config.user_id = "testuser"
        config.user_password = "testpass"

        session_creds = SessionProvider.factory(config)
        self.assertEqual("fAkESesSiOnId..", session_creds.session_id)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
        self.assertEqual("testentity", session_creds.entity_id)

    @responses.activate
    def testFromSessionCredentials(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid></locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.session_id = "fAkESesSiOnId.."

        session_creds = SessionProvider.factory(config)
        self.assertEqual("fAkESesSiOnId..", session_creds.session_id)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
        self.assertIsNone(session_creds.entity_id)

    @responses.activate
    def testFromTopLevelSessionCredentialsWithEntityOverride(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid>testentity</locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.session_id = "fAkESesSiOnId.."
        config.entity_id = "testentity"

        session_creds = SessionProvider.factory(config)
        self.assertEqual("fAkESesSiOnId..", session_creds.session_id)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
        self.assertEqual("testentity", session_creds.entity_id)

    @responses.activate
    def testFromPrivateLevelSessionCredentialsWithDifferentEntityOverride(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid>entityA</locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>EntityBSession..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid>entityB</locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsenderid"
        config.sender_password = "pass123!"
        config.session_id = "EntityAsession.."
        config.entity_id = "entityB"

        session_creds = SessionProvider.factory(config)
        self.assertEqual("EntityBSession..", session_creds.session_id)
        self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
        self.assertEqual("entityB", session_creds.entity_id)

    @responses.activate
    def testFromSessionCredentialsUsingEnvironmentSender(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>sessionProvider</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>testuser</userid>
                  <companyid>testcompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-12-06T15:57:08-08:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getSession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://unittest.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid></locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        with patch.dict('os.environ', {
            'INTACCT_SENDER_ID': 'envsender',
            'INTACCT_SENDER_PASSWORD': 'envpass',
        }):
            config = ClientConfig()
            config.session_id = "fAkESesSiOnId.."

            session_creds = SessionProvider.factory(config)
            self.assertEqual("fAkESesSiOnId..", session_creds.session_id)
            self.assertEqual("https://unittest.intacct.com/ia/xml/xmlgw.phtml", session_creds.endpoint_url)
            self.assertEqual("envsender", session_creds.sender_id)
            self.assertEqual("envpass", session_creds.sender_password)

