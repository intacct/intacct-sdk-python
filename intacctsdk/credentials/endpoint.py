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

import os
from urllib.parse import urlparse

from intacctsdk.client_config import ClientConfig


class Endpoint:

    DEFAULT_ENDPOINT = "https://api.intacct.com/ia/xml/xmlgw.phtml"

    ENDPOINT_URL_ENV_NAME = "INTACCT_ENDPOINT_URL"

    DOMAIN_NAME = "intacct.com"

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if value is None or value == "":
            value = self.DEFAULT_ENDPOINT

        test = urlparse(value)
        check = "." + self.DOMAIN_NAME
        if test.hostname[-len(check):] != check:
            raise Exception("Endpoint URL is not a valid " + self.DOMAIN_NAME + " domain name.")

        self._url = value

    def __init__(self, config: ClientConfig):
        if config.endpoint_url is None:
            self.url = os.getenv(self.ENDPOINT_URL_ENV_NAME)
        else:
            self.url = config.endpoint_url
