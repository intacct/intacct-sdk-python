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

from intacctsdk.xmls.request.session_authentication import SessionAuthentication
from tests.xmls.xml_object_test_helper import XmlObjectTestHelper


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
