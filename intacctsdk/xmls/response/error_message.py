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

import re
from xml.etree.ElementTree import Element


class ErrorMessage:

    @property
    def errors(self):
        return self._errors

    def __init__(self, error_messages: Element):
        self._errors = []

        error_contents = []
        for error_element in error_messages.findall("error"):
            pieces = ErrorMessage.combine_error_message_elements(error_element)
            error_contents.append(" ".join(pieces))

        self._errors = error_contents

    @staticmethod
    def combine_error_message_elements(error_element: Element):
        pieces = []
        for error_field in list(error_element):
            value = error_field.text
            if value is not None:
                piece = ErrorMessage.cleanse(value)
                pieces.append(piece)

        return pieces

    @staticmethod
    def cleanse(message: str) -> str:
        no_html = re.sub('<[^<]+?>', '', message)
        no_space = re.sub(' {2,}', ' ', no_html)

        return no_space
