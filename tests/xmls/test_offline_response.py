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
from intacctsdk.xmls.offline_response import OfflineResponse


class TestOfflineResponse(TestCase):

    def testParseResponse(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
      <acknowledgement>
            <status>success</status>
      </acknowledgement>
      <control>
            <status>success</status>
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
      </control>
</response>"""

        response = OfflineResponse(xml)
        self.assertEqual("success", response.status)

    def testThrowExceptionWithMissingAcknowledgementBlock(self):
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
            response = OfflineResponse(xml)

        self.assertEqual('Response block is missing acknowledgement block',
                         str(cm.exception))

    def testThrowExceptionWithMissingStatus(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <acknowledgement />
    <control>
        <status>success</status>
        <senderid>testsenderid</senderid>
        <controlid>ControlIdHere</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
    </control>
</response>"""
        with self.assertRaises(IntacctException) as cm:
            response = OfflineResponse(xml)

        self.assertEqual('Acknowledgement block is missing status element',
                         str(cm.exception))
