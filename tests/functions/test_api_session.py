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

from intacctsdk.functions.api_session import ApiSessionCreate
from tests.xmls.xml_object_test_helper import XmlObjectTestHelper


class TestApiSession(TestCase):

    def testApiSessionCreate(self):
        xml = """<?xml version="1.0" ?>
<test>
    <function controlid="unittest">
        <getAPISession/>
    </function>
</test>
"""

        record = ApiSessionCreate()
        record.control_id = "unittest"

        XmlObjectTestHelper.compare_xml(self, xml, record)

    def testApiSessionCreateWithLocationId(self):
        xml = """<?xml version="1.0" ?>
<test>
    <function controlid="unittest">
        <getAPISession>
            <locationid>100</locationid>
        </getAPISession>
    </function>
</test>
"""

        record = ApiSessionCreate()
        record.control_id = "unittest"
        record.entity_id = "100"

        XmlObjectTestHelper.compare_xml(self, xml, record)

    def testApiSessionCreateWithEmptyLocationId(self):
        xml = """<?xml version="1.0" ?>
<test>
    <function controlid="unittest">
        <getAPISession>
            <locationid/>
        </getAPISession>
    </function>
</test>
"""

        record = ApiSessionCreate()
        record.control_id = "unittest"
        record.entity_id = ""

        XmlObjectTestHelper.compare_xml(self, xml, record)
