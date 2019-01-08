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

from intacctsdk.client_config import ClientConfig
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.request.control_block import ControlBlock
from tests.xmls.xml_object_test_helper import XmlObjectTestHelper


class TestControlBlock(TestCase):

    def testDefaults(self):
        client_config = ClientConfig()
        client_config.sender_id = "testsenderid"
        client_config.sender_password = "pass123!"

        request_config = RequestConfig()
        request_config.control_id = "unittest"

        expected = """<?xml version="1.0" ?>
<test>
    <control>
        <senderid>testsenderid</senderid>
        <password>pass123!</password>
        <controlid>unittest</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
        <includewhitespace>false</includewhitespace>
    </control>
</test>
"""
        control = ControlBlock(client_config, request_config)

        XmlObjectTestHelper.compare_xml(self, expected, control)

    def testExceptionWhenSenderIdBlank(self):
        client_config = ClientConfig()

        request_config = RequestConfig()

        with self.assertRaises(Exception) as cm:
            control = ControlBlock(client_config, request_config)

        self.assertEqual("Sender ID is required and cannot be blank",
                         str(cm.exception))

    def testExceptionWhenSenderPasswordBlank(self):
        client_config = ClientConfig()
        client_config.sender_id = "testsenderid"

        request_config = RequestConfig()

        with self.assertRaises(Exception) as cm:
            control = ControlBlock(client_config, request_config)

        self.assertEqual("Sender Password is required and cannot be blank",
                         str(cm.exception))

    def testOverridingDefaults(self):
        client_config = ClientConfig()
        client_config.sender_id = "testsenderid"
        client_config.sender_password = "pass123!"

        request_config = RequestConfig()
        request_config.control_id = "testcontrol"
        request_config.unique_id = True
        request_config.policy_id = "testpolicy"

        expected = """<?xml version="1.0" ?>
<test>
    <control>
        <senderid>testsenderid</senderid>
        <password>pass123!</password>
        <controlid>testcontrol</controlid>
        <uniqueid>true</uniqueid>
        <dtdversion>3.0</dtdversion>
        <policyid>testpolicy</policyid>
        <includewhitespace>false</includewhitespace>
    </control>
</test>
"""
        control = ControlBlock(client_config, request_config)

        XmlObjectTestHelper.compare_xml(self, expected, control)

    def testExceptionWhenControlIdTooLong(self):
        client_config = ClientConfig()
        client_config.sender_id = "testSender"
        client_config.sender_password = "testPassword"

        request_config = RequestConfig()
        request_config.control_id = "12345678901234567890123456789012345678901234567890123456789012345678901234567890" \
                                    + "123456789012345678901234567890123456789012345678901234567890123456789" \
                                    + "123456789012345678901234567890123456789012345678901234567890123456789" \
                                    + "123456789012345678901234567890123456789012345678901234567890123456789" \
                                    + "012345678900123456789001234567890012345678900123456789001234567890"
        with self.assertRaises(Exception) as cm:
            control = ControlBlock(client_config, request_config)

        self.assertEqual('Request control ID must be between 1 and 256 characters in length.',
                         str(cm.exception))
