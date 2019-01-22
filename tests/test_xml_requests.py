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

from intacctsdk.configs import ClientConfig, RequestConfig
from intacctsdk.functions import ApiSessionCreate
from intacctsdk.xml_requests import RequestBlock, ControlBlock, OperationBlock, LoginAuthentication, SessionAuthentication
from tests.helpers import XmlObjectTestHelper


class TestRequestBlock(TestCase):

    def testGenerateFullRequestXmlBlock(self):
        expected = """<request><control><senderid>testsenderid</senderid><password>pass123!</password><controlid>unittest</controlid><uniqueid>false</uniqueid><dtdversion>3.0</dtdversion><includewhitespace>false</includewhitespace></control><operation transaction="false"><authentication><sessionid>testsession..</sessionid></authentication><content /></operation></request>"""

        client_config = ClientConfig()
        client_config.sender_id = "testsenderid"
        client_config.sender_password = "pass123!"
        client_config.session_id = "testsession.."

        request_config = RequestConfig()
        request_config.control_id = "unittest"

        content_block = []

        request_block = RequestBlock(client_config, request_config, content_block)

        actual = request_block.write_xml().decode()

        self.assertEqual(expected, actual)


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


class TestOperationBlock(TestCase):

    def testSessionAuth(self):
        client_config = ClientConfig()
        client_config.session_id = "fakesession.."

        request_config = RequestConfig()
        api_func = ApiSessionCreate()
        api_func.control_id = "unittest"
        content = [
            api_func,
        ]

        expected = """<?xml version="1.0" ?>
<test>
    <operation transaction="false">
        <authentication>
            <sessionid>fakesession..</sessionid>
        </authentication>
        <content>
            <function controlid="unittest">
                <getAPISession/>
            </function>
        </content>
    </operation>
</test>
"""
        control = OperationBlock(client_config, request_config, content)

        XmlObjectTestHelper.compare_xml(self, expected, control)

    def testLoginAuth(self):
        client_config = ClientConfig()
        client_config.company_id = "testcompany"
        client_config.user_id = "testuser"
        client_config.user_password = "testpass"

        request_config = RequestConfig()
        api_func = ApiSessionCreate()
        api_func.control_id = "unittest"
        content = [
            api_func,
        ]

        expected = """<?xml version="1.0" ?>
<test>
    <operation transaction="false">
        <authentication>
            <login>
                <userid>testuser</userid>
                <companyid>testcompany</companyid>
                <password>testpass</password>
            </login>
        </authentication>
        <content>
            <function controlid="unittest">
                <getAPISession/>
            </function>
        </content>
    </operation>
</test>
"""
        control = OperationBlock(client_config, request_config, content)

        XmlObjectTestHelper.compare_xml(self, expected, control)

    def testOperationTransactionTrue(self):
        client_config = ClientConfig()
        client_config.session_id = "fakesession.."

        request_config = RequestConfig()
        request_config.transaction = True

        api_func = ApiSessionCreate()
        api_func.control_id = "unittest"
        content = [
            api_func,
        ]

        expected = """<?xml version="1.0" ?>
<test>
    <operation transaction="true">
        <authentication>
            <sessionid>fakesession..</sessionid>
        </authentication>
        <content>
            <function controlid="unittest">
                <getAPISession/>
            </function>
        </content>
    </operation>
</test>
"""
        control = OperationBlock(client_config, request_config, content)

        XmlObjectTestHelper.compare_xml(self, expected, control)

    def testExceptionWhenNoAuthCredsProvided(self):
        client_config = ClientConfig()
        request_config = RequestConfig()

        with self.assertRaises(Exception) as cm:
            operation = OperationBlock(client_config, request_config, [])

        self.assertEqual(
            "Authentication credentials [Company ID, User ID, and User Password] or [Session ID] "
            + "are required and cannot be blank.",
            str(cm.exception))


class TestLoginAuthentication(TestCase):

    def testCompanyIdUserIdPassword(self):
        expected = """<?xml version="1.0" ?>
<test>
    <authentication>
        <login>
            <userid>testuser</userid>
            <companyid>testcompany</companyid>
            <password>testpass</password>
        </login>
    </authentication>
</test>
"""
        auth = LoginAuthentication("testuser", "testcompany", "testpass")

        XmlObjectTestHelper.compare_xml(self, expected, auth)

    def testCompanyIdEntityIdUserIdPassword(self):
        expected = """<?xml version="1.0" ?>
<test>
    <authentication>
        <login>
            <userid>testuser</userid>
            <companyid>testcompany</companyid>
            <password>testpass</password>
            <locationid>testentity</locationid>
        </login>
    </authentication>
</test>
"""
        auth = LoginAuthentication("testuser", "testcompany", "testpass", "testentity")

        XmlObjectTestHelper.compare_xml(self, expected, auth)

    def testCompanyIdEmptyEntityIdUserIdPassword(self):
        expected = """<?xml version="1.0" ?>
<test>
    <authentication>
        <login>
            <userid>testuser</userid>
            <companyid>testcompany</companyid>
            <password>testpass</password>
            <locationid/>
        </login>
    </authentication>
</test>
"""
        auth = LoginAuthentication("testuser", "testcompany", "testpass", "")

        XmlObjectTestHelper.compare_xml(self, expected, auth)

    def testExceptionWhenCompanyIdNull(self):
        with self.assertRaises(Exception) as cm:
            auth = LoginAuthentication("testuser", "", "testpass")

        self.assertEqual("Company ID is required and cannot be blank",
                         str(cm.exception))

    def testExceptionWhenUserIdNull(self):
        with self.assertRaises(Exception) as cm:
            auth = LoginAuthentication("", "testcompany", "testpass")

        self.assertEqual("User ID is required and cannot be blank",
                         str(cm.exception))

    def testExceptionWhenPasswordNull(self):
        with self.assertRaises(Exception) as cm:
            auth = LoginAuthentication("testuser", "testcompany", "")

        self.assertEqual("User Password is required and cannot be blank",
                         str(cm.exception))


class TestSessionAuthentication(TestCase):

    def testCompanyIdUserIdPassword(self):
        expected = """<?xml version="1.0" ?>
<test>
    <authentication>
        <sessionid>testsessionid..</sessionid>
    </authentication>
</test>
"""
        auth = SessionAuthentication("testsessionid..")

        XmlObjectTestHelper.compare_xml(self, expected, auth)

    def testExceptionWhenSessionIdNull(self):
        with self.assertRaises(Exception) as cm:
            auth = SessionAuthentication("")

        self.assertEqual("Session ID is required and cannot be blank",
                         str(cm.exception))
