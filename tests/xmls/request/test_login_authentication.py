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

from intacctsdk.xmls.request.login_authentication import LoginAuthentication
from tests.xmls.xml_object_test_helper import XmlObjectTestHelper


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
