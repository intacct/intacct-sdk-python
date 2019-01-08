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
from intacctsdk.functions.api_session import ApiSessionCreate
from intacctsdk.request_config import RequestConfig
from intacctsdk.xmls.request.operation_block import OperationBlock
from tests.xmls.xml_object_test_helper import XmlObjectTestHelper


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
