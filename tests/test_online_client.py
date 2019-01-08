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

from intacctsdk.client_config import ClientConfig
from intacctsdk.exceptions.result_exception import ResultException
from intacctsdk.functions.api_session import ApiSessionCreate
from intacctsdk.online_client import OnlineClient
from intacctsdk.request_config import RequestConfig


class TestOnlineClient(TestCase):

    @responses.activate
    def testExecuteRequest(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
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

        client = OnlineClient(config)

        response = client.execute(ApiSessionCreate('func1UnitTest'))
        self.assertEqual("requestUnitTest", response.control.control_id)

    @responses.activate
    def testExecuteRequestAndThrowResultException(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
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
                  <status>failure</status>
                  <function>getAPISession</function>
                  <controlid>func1UnitTest</controlid>
                  <errormessage>
                        <error>
                              <errorno>Get API Session Failed</errorno>
                              <description></description>
                              <description2>Something went wrong</description2>
                              <correction></correction>
                        </error>
                  </errormessage>
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

        client = OnlineClient(config)
        with self.assertRaises(ResultException) as cm:
            client.execute(ApiSessionCreate('func1UnitTest'))

        self.assertEqual("Result status: failure for Control ID: func1UnitTest", str(cm.exception))

    @responses.activate
    def testExecuteBatchRequestAndThrowResultException(self):
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
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
                  <status>aborted</status>
                  <function>getAPISession</function>
                  <controlid>func1UnitTest</controlid>
                  <errormessage>
                          <error>
                                <errorno>XL03000009</errorno>
                                <description></description>
                                <description2>The entire transaction in this operation has been rolled back due to an error.</description2>
                                <correction></correction>
                          </error>
                  </errormessage>
            </result>
            <result>
                  <status>failure</status>
                  <function>getAPISession</function>
                  <controlid>func2UnitTest</controlid>
                  <errormessage>
                        <error>
                              <errorno>Get API Session Failed</errorno>
                              <description></description>
                              <description2>Something went wrong</description2>
                              <correction></correction>
                        </error>
                          <error>
                                <errorno>XL03000009</errorno>
                                <description></description>
                                <description2>The entire transaction in this operation has been rolled back due to an error.</description2>
                                <correction></correction>
                          </error>
                  </errormessage>
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

        client = OnlineClient(config)
        funcs = [
            ApiSessionCreate('func1UnitTest'),
            ApiSessionCreate('func2UnitTest'),
        ]

        with self.assertRaises(ResultException) as cm:
            client.execute_batch(funcs, request_config)

        self.assertEqual("Result status: failure for Control ID: func2UnitTest", str(cm.exception))

    # TODO logging test
