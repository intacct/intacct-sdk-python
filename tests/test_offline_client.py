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
from intacctsdk.functions.api_session import ApiSessionCreate
from intacctsdk.offline_client import OfflineClient
from intacctsdk.request_config import RequestConfig


class TestOfflineClient(TestCase):

    @responses.activate
    def testExecuteRequest(self):
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
        request_config.policy_id = "asyncPolicyId"

        client = OfflineClient(config)

        response = client.execute(ApiSessionCreate('func1UnitTest'), request_config)
        self.assertEqual("requestUnitTest", response.control.control_id)

    @responses.activate
    def testExecuteBatchRequest(self):
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
        request_config.policy_id = "asyncPolicyId"

        client = OfflineClient(config)

        funcs = [
            ApiSessionCreate('func1UnitTest'),
        ]
        response = client.execute_batch(funcs, request_config)
        self.assertEqual("requestUnitTest", response.control.control_id)
