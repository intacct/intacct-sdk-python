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

import logging
import responses
from unittest import TestCase

from intacctsdk.configs import ClientConfig, RequestConfig
from intacctsdk.exceptions import ResponseException
from intacctsdk.functions import ApiSessionCreate
from intacctsdk.handlers import RequestHandler
from intacctsdk.xml_responses import OnlineResponse, OfflineResponse


class TestRequestHandler(TestCase):

    @responses.activate
    def testReturnsOnlineResponse(self):
        xml_response = """<?xml version="1.0" encoding="utf-8" ?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>requestUnitTest</controlid>
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
                  <function>getAPISession</function>
                  <controlid>func1UnitTest</controlid>
                  <data>
                        <api>
                              <sessionid>unittest..</sessionid>
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
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.control_id = "unittest"

        request_handler = RequestHandler(config, request_config)
        response = request_handler.execute_online([ApiSessionCreate()])
        self.assertIsInstance(response, OnlineResponse)

    @responses.activate
    def testReturnsOfflineResponse(self):
        xml_response = """<?xml version="1.0" encoding="utf-8" ?>
<response>
      <acknowledgement>
            <status>success</status>
      </acknowledgement>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>requestUnitTest</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.policy_id = "policyid123"
        request_config.control_id = "unittest"

        request_handler = RequestHandler(config, request_config)
        response = request_handler.execute_offline([ApiSessionCreate()])
        self.assertIsInstance(response, OfflineResponse)

    @responses.activate
    def testExceptionWhenPolicyIdNotIncludedForOfflineRequest(self):
        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.control_id = "unittest"

        request_handler = RequestHandler(config, request_config)
        with self.assertRaises(Exception) as cm:
            response = request_handler.execute_offline([ApiSessionCreate()])

        self.assertEqual("Required Policy ID not supplied in config for offline request", str(cm.exception))

    @responses.activate
    def testReturnsOnlineResponseAfterRetry(self):
        xml_response = """<?xml version="1.0" encoding="utf-8" ?>
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
                  <function>getAPISession</function>
                  <controlid>func1UnitTest</controlid>
                  <data>
                        <api>
                              <sessionid>unittest..</sessionid>
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

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', status=502)

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()

        request_handler = RequestHandler(config, request_config)
        response = request_handler.execute_online([ApiSessionCreate()])
        self.assertIsInstance(response, OnlineResponse)

    @responses.activate
    def testErrorAfterMultipleRetries(self):
        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', status=503)
        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', status=503)
        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', status=503)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.max_retries = 2

        request_handler = RequestHandler(config, request_config)

        with self.assertRaises(Exception) as cm:
            response = request_handler.execute_online([ApiSessionCreate()])

        self.assertEqual("Request retry count exceeded max retry count: 2",
                         str(cm.exception))

    @responses.activate
    def test400LevelErrorWithXmlResponse(self):
        xml_response = """<?xml version="1.0" encoding="utf-8" ?>
<response>
    <control>
        <status>failure</status>
    </control>
    <errormessage>
        <error>
            <errorno>XMLGW_JPP0002</errorno>
            <description>Sign-in information is incorrect. Please check your request.</description>
        </error>
    </errormessage>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=401,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()

        request_handler = RequestHandler(config, request_config)

        with self.assertRaises(ResponseException) as cm:
            response = request_handler.execute_online([ApiSessionCreate()])

        self.assertEqual("Response control status failure", str(cm.exception))

    @responses.activate
    def testErrorAfter524ServerError(self):
        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', status=524)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()

        request_handler = RequestHandler(config, request_config)

        with self.assertRaises(Exception) as cm:
            response = request_handler.execute_online([ApiSessionCreate()])

        self.assertEqual("524 Server Error: None for url: https://api.intacct.com/ia/xml/xmlgw.phtml",
                         str(cm.exception))

    @responses.activate
    def testExecutesWithDebugLogger(self):
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
                  <function>getAPISession</function>
                  <controlid>func1UnitTest</controlid>
                  <data>
                        <api>
                              <sessionid>unittest..</sessionid>
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
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.transaction = True

        content = [
            ApiSessionCreate('func1UnitTest'),
        ]

        handler = RequestHandler(config, request_config)

        with self.assertLogs(logging.getLogger(), logging.DEBUG) as cm:
            handler.execute_online(content)

        self.assertTrue("intacct-sdk-python-client/" in cm.records[0].getMessage())

    @responses.activate
    def testExecuteOfflineWithSessionCreds(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <acknowledgement>
            <status>success</status>
      </acknowledgement>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>requestUnitTest</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
</response>"""
        headers = {
            "Content-Type": 'text/xml; encoding="UTF-8"',
        }

        responses.add(responses.POST, 'https://api.intacct.com/ia/xml/xmlgw.phtml', body=xml_response, status=200,
                      headers=headers)

        config = ClientConfig()
        config.sender_id = "testsender"
        config.sender_password = "testsendpass"
        config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.transaction = True
        request_config.policy_id = "policyid123"

        content = [
            ApiSessionCreate('func1UnitTest'),
        ]

        handler = RequestHandler(config, request_config)

        with self.assertLogs(logging.getLogger(), logging.DEBUG) as cm:
            handler.execute_offline(content)

        self.assertEqual(2, len(cm.records))
        self.assertTrue("Offline execution sent to Intacct using Session-based credentials." in cm.records[0].getMessage())
        self.assertEqual(logging.WARNING, cm.records[0].levelno)
