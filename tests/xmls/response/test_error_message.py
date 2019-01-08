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

from intacctsdk.xmls.response.error_message import ErrorMessage


class TestErrorMessage(TestCase):

    def testParseErrors(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<errormessage>
    <error>
          <errorno>1234</errorno>
          <description>description</description>
          <description2>Object definition &#39;BADOBJECT&#39; not found.</description2>
          <correction>strip&lt;out&gt;these&lt;/out&gt;tags.</correction>
    </error>
    <error>
          <errorno>5678</errorno>
          <description>strip&lt;out&gt;these&lt;/out&gt;tags.</description>
          <description2>Object definition &#39;BADOBJECT&#39; not found.</description2>
          <correction>correct.</correction>
    </error>
</errormessage>"""

        xml_element = ElementTree.fromstring(xml)
        error_message = ErrorMessage(xml_element)

        self.assertEqual(2, len(error_message.errors))
        self.assertEqual("1234 description Object definition 'BADOBJECT' not found. stripthesetags.",
                         error_message.errors[0])
        self.assertEqual("5678 stripthesetags. Object definition 'BADOBJECT' not found. correct.",
                         error_message.errors[1])
