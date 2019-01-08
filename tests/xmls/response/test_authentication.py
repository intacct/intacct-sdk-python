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
from intacctsdk.xmls.response.authentication import Authentication


class TestAuthentication(TestCase):

    def testParseResponse(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<authentication>
    <status>success</status>
    <userid>fakeuser</userid>
    <companyid>fakecompany</companyid>
    <locationid></locationid>
    <sessiontimestamp>2015-10-24T18:56:52-07:00</sessiontimestamp>
</authentication>"""

        authentication = Authentication(ElementTree.fromstring(xml))
        self.assertEqual("success", authentication.status)
        self.assertEqual("fakeuser", authentication.user_id)
        self.assertEqual("fakecompany", authentication.company_id)
        self.assertIsNone(authentication.entity_id)

    def testThrowExceptionWhenStatusNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<authentication>
    <!--<status>success</status>-->
    <userid>fakeuser</userid>
    <companyid>fakecompany</companyid>
    <locationid></locationid>
    <sessiontimestamp>2015-10-24T18:56:52-07:00</sessiontimestamp>
</authentication>"""

        with self.assertRaises(IntacctException) as cm:
            authentication = Authentication(ElementTree.fromstring(xml))

        self.assertEqual('Authentication block is missing status element',
                         str(cm.exception))

    def testThrowExceptionWhenUserIdNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<authentication>
    <status>success</status>
    <!--<userid>fakeuser</userid>-->
    <companyid>fakecompany</companyid>
    <locationid></locationid>
    <sessiontimestamp>2015-10-24T18:56:52-07:00</sessiontimestamp>
</authentication>"""

        with self.assertRaises(IntacctException) as cm:
            authentication = Authentication(ElementTree.fromstring(xml))

        self.assertEqual('Authentication block is missing userid element',
                         str(cm.exception))

    def testThrowExceptionWhenCompanyIdNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<authentication>
    <status>success</status>
    <userid>fakeuser</userid>
    <!--<companyid>fakecompany</companyid>-->
    <locationid></locationid>
    <sessiontimestamp>2015-10-24T18:56:52-07:00</sessiontimestamp>
</authentication>"""

        with self.assertRaises(IntacctException) as cm:
            authentication = Authentication(ElementTree.fromstring(xml))

        self.assertEqual('Authentication block is missing companyid element',
                         str(cm.exception))
