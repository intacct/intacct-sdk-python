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

from xml.etree import ElementTree
from unittest import TestCase
from xml.dom import minidom


class XmlObjectTestHelper:

    @staticmethod
    def compare_xml(test_case: TestCase, expected: str, api_function: ElementTree):
        test = ElementTree.Element("test")

        api_function.write_xml(test)

        actual = minidom.parseString(ElementTree.tostring(test)).toprettyxml(indent="    ")

        test_case.assertEqual(expected, actual)
