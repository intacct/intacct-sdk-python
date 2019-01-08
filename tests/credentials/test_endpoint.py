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
from unittest.mock import patch

from intacctsdk.client_config import ClientConfig
from intacctsdk.credentials.endpoint import Endpoint


class TestEndpoint(TestCase):

    def testDefaultEndpoint(self):
        config = ClientConfig()
        endpoint = Endpoint(config)

        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testEnvEndpoint(self):
        with patch.dict('os.environ', {'INTACCT_ENDPOINT_URL': 'https://envunittest.intacct.com/ia/xml/xmlgw.phtml'}):
            config = ClientConfig()
            endpoint = Endpoint(config)

            self.assertEqual("https://envunittest.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testConfigEndpoint(self):
        config = ClientConfig()
        config.endpoint_url = "https://configtest.intacct.com/ia/xml/xmlgw.phtml"
        endpoint = Endpoint(config)

        self.assertEqual("https://configtest.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testDefaultEndpointIfConfigIsNull(self):
        config = ClientConfig()
        config.endpoint_url = ""
        endpoint = Endpoint(config)

        self.assertEqual("https://api.intacct.com/ia/xml/xmlgw.phtml", endpoint.url)

    def testInvalidEndpointException(self):
        config = ClientConfig()
        config.endpoint_url = "https://www.example.com/xmlgw.phtml"
        with self.assertRaises(Exception) as cm:
            endpoint = Endpoint(config)

        self.assertEqual("Endpoint URL is not a valid intacct.com domain name.", str(cm.exception))
