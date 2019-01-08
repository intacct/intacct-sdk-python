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

from intacctsdk.exceptions.intacct_exception import IntacctException
from intacctsdk.exceptions.response_exception import ResponseException
from intacctsdk.xmls.online_response import OnlineResponse
from intacctsdk.xmls.response.result import Result


class TestOnlineResponse(TestCase):

    def testParseResponse(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>fakeuser</userid>
                  <companyid>fakecompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-10-22T20:58:27-07:00</sessiontimestamp>
            </authentication>
            <result>
                  <status>success</status>
                  <function>getAPISession</function>
                  <controlid>testControlId</controlid>
                  <data>
                        <api>
                              <sessionid>fAkESesSiOnId..</sessionid>
                              <endpoint>https://api.intacct.com/ia/xml/xmlgw.phtml</endpoint>
                              <locationid></locationid>
                        </api>
                  </data>
            </result>
      </operation>
</response>"""

        response = OnlineResponse(xml)
        self.assertEqual(1, len(response.results))
        self.assertIsInstance(response.results[0], Result)

    def testThrowExceptionWithMissingOperationBlock(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
</response>"""
        with self.assertRaises(IntacctException) as cm:
            response = OnlineResponse(xml)

        self.assertEqual('Response block is missing operation block',
                         str(cm.exception))

    def testThrowExceptionWithAuthFailure(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>failure</status>
                  <userid>fakeuser</userid>
                  <companyid>fakecompany</companyid>
                  <locationid></locationid>
            </authentication>
            <errormessage>
                  <error>
                        <errorno>XL03000006</errorno>
                        <description></description>
                        <description2>Sign-in information is incorrect</description2>
                        <correction></correction>
                  </error>
            </errormessage>
      </operation>
</response>"""
        with self.assertRaises(ResponseException) as cm:
            response = OnlineResponse(xml)

        self.assertEqual('Response authentication status failure',
                         str(cm.exception))

    def testThrowExceptionWithMissingAuthBlock(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation/>
</response>"""
        with self.assertRaises(IntacctException) as cm:
            response = OnlineResponse(xml)

        self.assertEqual('Authentication block is missing from operation element',
                         str(cm.exception))

    def testThrowExceptionWithMissingResultBlock(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
      <operation>
            <authentication>
                  <status>success</status>
                  <userid>fakeuser</userid>
                  <companyid>fakecompany</companyid>
                  <locationid></locationid>
                  <sessiontimestamp>2015-10-22T20:58:27-07:00</sessiontimestamp>
            </authentication>
      </operation>
</response>"""
        with self.assertRaises(IntacctException) as cm:
            response = OnlineResponse(xml)

        self.assertEqual('Result block is missing from operation element',
                         str(cm.exception))

    def testThrowResponseExceptionWithErrors(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <control>
        <status>failure</status>
        <senderid></senderid>
        <controlid></controlid>
    </control>
    <errormessage>
        <error>
            <errorno>PL04000055</errorno>
            <description></description>
            <description2>This company is a demo company and has expired.</description2>
            <correction></correction>
        </error>
    </errormessage>
</response>"""
        with self.assertRaises(ResponseException) as cm:
            response = OnlineResponse(xml)

        self.assertEqual('Response control status failure',
                         str(cm.exception))
        self.assertEqual(1, len(cm.exception.errors))
