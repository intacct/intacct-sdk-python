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
from intacctsdk.exceptions.result_exception import ResultException
from intacctsdk.xmls.response.result import Result


class TestResult(TestCase):

    def testSuccessResult(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>success</status>
    <function>readByQuery</function>
    <controlid>testControlId</controlid>
    <data listtype="department" count="0" totalcount="0" numremaining="0" resultId=""/>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual("success", result.status)
        self.assertEqual("readByQuery", result.function_name)
        self.assertEqual("testControlId", result.control_id)

    def testFailureStatusAndError(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
      <status>failure</status>
      <function>readByQuery</function>
      <controlid>testControlId</controlid>
      <errormessage>
            <error>
                  <errorno>Query Failed</errorno>
                  <description></description>
                  <description2>Object definition BADOBJECT not found</description2>
                  <correction></correction>
            </error>
      </errormessage>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual("failure", result.status)
        self.assertEqual(1, len(result.errors))

    def testThrowExceptionWhenStatusNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
      <!--<status>success</status>-->
      <function>readByQuery</function>
      <controlid>testControlId</controlid>
      <data listtype="department" count="0" totalcount="0" numremaining="0" resultId="" />
</result>"""

        with self.assertRaises(IntacctException) as cm:
            result = Result(ElementTree.fromstring(xml))

        self.assertEqual('Response result block is missing status element',
                         str(cm.exception))

    def testThrowExceptionWhenFunctionNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
      <status>success</status>
      <!--<function>readByQuery</function>-->
      <controlid>testControlId</controlid>
      <data listtype="department" count="0" totalcount="0" numremaining="0" resultId="" />
</result>"""

        with self.assertRaises(IntacctException) as cm:
            result = Result(ElementTree.fromstring(xml))

        self.assertEqual('Response result block is missing function element',
                         str(cm.exception))

    def testThrowExceptionWhenControlIdNotIncluded(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
      <status>success</status>
      <function>readByQuery</function>
      <!--<controlid>testControlId</controlid>-->
      <data listtype="department" count="0" totalcount="0" numremaining="0" resultId="" />
</result>"""

        with self.assertRaises(IntacctException) as cm:
            result = Result(ElementTree.fromstring(xml))

        self.assertEqual('Response result block is missing controlid element',
                         str(cm.exception))

    def testThrowExceptionWhenStatusFailure(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>failure</status>
    <function>read</function>
    <controlid>testControlId</controlid>
    <errormessage>
        <error>
            <errorno>XXX</errorno>
            <description></description>
            <description2>Object definition VENDOR2 not found</description2>
            <correction></correction>
        </error>
    </errormessage>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        with self.assertRaises(ResultException) as cm:
            result.ensure_status_not_failure()

        self.assertEqual('Result status: failure for Control ID: testControlId',
                         str(cm.exception))

    def testThrowExceptionWhenStatusAborted(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>aborted</status>
    <function>readByQuery</function>
    <controlid>testFunctionId</controlid>
    <errormessage>
        <error>
            <errorno>Query Failed</errorno>
            <description></description>
            <description2>Object definition VENDOR9 not found</description2>
            <correction></correction>
        </error>
        <error>
            <errorno>XL03000009</errorno>
            <description></description>
            <description2>The entire transaction in this operation has been rolled back due to an error.</description2>
            <correction></correction>
        </error>
    </errormessage>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        with self.assertRaises(ResultException) as cm:
            result.ensure_status_success()

        self.assertEqual('Result status: aborted for Control ID: testFunctionId',
                         str(cm.exception))

    def testNotThrowExceptionWhenStatusAborted(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>aborted</status>
    <function>readByQuery</function>
    <controlid>testFunctionId</controlid>
    <errormessage>
        <error>
            <errorno>Query Failed</errorno>
            <description></description>
            <description2>Object definition VENDOR9 not found</description2>
            <correction></correction>
        </error>
        <error>
            <errorno>XL03000009</errorno>
            <description></description>
            <description2>The entire transaction in this operation has been rolled back due to an error.</description2>
            <correction></correction>
        </error>
    </errormessage>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        result.ensure_status_not_failure()

    def testParseGetListClassResponse(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>success</status>
    <function>get_list</function>
    <controlid>ccdeafa7-4f22-49ae-b6ae-b5e1a39423e7</controlid>
    <listtype start="0" end="1" total="2">class</listtype>
    <data>
        <class>
            <key>C1234</key>
            <name>hello world</name>
            <description/>
            <parentid/>
            <whenmodified>07/24/2018 15:19:46</whenmodified>
            <status>active</status>
        </class>
        <class>
            <key>C1235</key>
            <name>hello world</name>
            <description/>
            <parentid/>
            <whenmodified>07/24/2018 15:20:27</whenmodified>
            <status>active</status>
        </class>
    </data>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual(0, result.start)
        self.assertEqual(1, result.end)
        self.assertEqual(2, result.total_count)
        self.assertEqual(2, len(result.data))

    def testParseReadByQueryClassResponse(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>success</status>
    <function>readByQuery</function>
    <controlid>818b0a96-3faf-4931-97e6-1cf05818ea44</controlid>
    <data listtype="class" count="1" totalcount="2" numremaining="1" resultId="myResultId">
        <class>
            <RECORDNO>8</RECORDNO>
            <CLASSID>C1234</CLASSID>
            <NAME>hello world</NAME>
            <DESCRIPTION></DESCRIPTION>
            <STATUS>active</STATUS>
            <PARENTKEY></PARENTKEY>
            <PARENTID></PARENTID>
            <PARENTNAME></PARENTNAME>
            <WHENCREATED>07/24/2017 15:19:46</WHENCREATED>
            <WHENMODIFIED>07/24/2017 15:19:46</WHENMODIFIED>
            <CREATEDBY>9</CREATEDBY>
            <MODIFIEDBY>9</MODIFIEDBY>
            <MEGAENTITYKEY></MEGAENTITYKEY>
            <MEGAENTITYID></MEGAENTITYID>
            <MEGAENTITYNAME></MEGAENTITYNAME>
        </class>
    </data>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual(1, result.count)
        self.assertEqual(2, result.total_count)
        self.assertEqual(1, result.num_remaining)
        self.assertEqual("myResultId", result.result_id)
        self.assertEqual(1, len(result.data))

    def testParseReadByQueryWithMultipleRecords(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>success</status>
    <function>readByQuery</function>
    <controlid>818b0a96-3faf-4931-97e6-1cf05818ea44</controlid>
    <data listtype="class" count="2" totalcount="3" numremaining="1" resultId="myResultId">
        <class>
            <RECORDNO>8</RECORDNO>
            <CLASSID>C1234</CLASSID>
            <NAME>hello world</NAME>
            <DESCRIPTION></DESCRIPTION>
            <STATUS>active</STATUS>
            <PARENTKEY></PARENTKEY>
            <PARENTID></PARENTID>
            <PARENTNAME></PARENTNAME>
            <WHENCREATED>07/24/2017 15:19:46</WHENCREATED>
            <WHENMODIFIED>07/24/2017 15:19:46</WHENMODIFIED>
            <CREATEDBY>9</CREATEDBY>
            <MODIFIEDBY>9</MODIFIEDBY>
            <MEGAENTITYKEY></MEGAENTITYKEY>
            <MEGAENTITYID></MEGAENTITYID>
            <MEGAENTITYNAME></MEGAENTITYNAME>
        </class>
        <class>
            <RECORDNO>9</RECORDNO>
            <CLASSID>C1235</CLASSID>
            <NAME>hello world2</NAME>
            <DESCRIPTION></DESCRIPTION>
            <STATUS>active</STATUS>
            <PARENTKEY></PARENTKEY>
            <PARENTID></PARENTID>
            <PARENTNAME></PARENTNAME>
            <WHENCREATED>07/24/2017 15:19:46</WHENCREATED>
            <WHENMODIFIED>07/24/2017 15:19:46</WHENMODIFIED>
            <CREATEDBY>9</CREATEDBY>
            <MODIFIEDBY>9</MODIFIEDBY>
            <MEGAENTITYKEY></MEGAENTITYKEY>
            <MEGAENTITYID></MEGAENTITYID>
            <MEGAENTITYNAME></MEGAENTITYNAME>
        </class>
    </data>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual(2, result.count)
        self.assertEqual(3, result.total_count)
        self.assertEqual(1, result.num_remaining)
        self.assertEqual("myResultId", result.result_id)
        self.assertEqual(2, len(result.data))

    def testParseLegacyCreateClassKey(self):
        xml = """<?xml version="1.0" encoding="utf-8" ?>
<result>
    <status>success</status>
    <function>create_class</function>
    <controlid>d4814563-1e97-4708-b9c5-9a49569d2a0d</controlid>
    <key>C1234</key>
</result>"""

        result = Result(ElementTree.fromstring(xml))
        self.assertEqual("C1234", result.key)
