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
from intacctsdk.xmls.request_block import RequestBlock


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
