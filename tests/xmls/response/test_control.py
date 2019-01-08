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
from xml.etree import ElementTree

from intacctsdk.exceptions.intacct_exception import IntacctException
from intacctsdk.xmls.response.control import Control


class TestControl(TestCase):

    def testParseResponse(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<control>
    <status>success</status>
    <senderid>testsenderid</senderid>
    <controlid>ControlIdHere</controlid>
    <uniqueid>false</uniqueid>
    <dtdversion>3.0</dtdversion>
</control>"""

        control = Control(ElementTree.fromstring(xml))
        self.assertEqual("testsenderid", control.sender_id)
        self.assertEqual("ControlIdHere", control.control_id)
        self.assertEqual("false", control.unique_id)
        self.assertEqual("3.0", control.dtd_version)

    def testThrowExceptionWhenStatusNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
        <control>
            <!--<status>success</status>-->
            <senderid>testsenderid</senderid>
            <controlid>ControlIdHere</controlid>
            <uniqueid>false</uniqueid>
            <dtdversion>3.0</dtdversion>
        </control>"""

        with self.assertRaises(IntacctException) as cm:
            control = Control(ElementTree.fromstring(xml))

        self.assertEqual('Control block is missing status element',
                         str(cm.exception))
