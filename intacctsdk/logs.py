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
import socket
from datetime import datetime
from requests import Response
from urllib3.util import parse_url


class MessageFormatter:

    @staticmethod
    def clf():
        return '{hostname} {req_header_User-Agent} - [{date_common_log}] ' \
               '{method} {target} HTTP/{version}" {code} {res_header_Content-Length}'

    @staticmethod
    def debug():
        return '>>>>>>>>\n{request}\n<<<<<<<<\n{response}\n--------\n{error}'

    @staticmethod
    def short():
        return '[{ts}] "{method} {target} HTTP/{version}" {code}'

    @staticmethod
    def headers(headers):
        result = ""
        for header_key, header_val in headers.items():
            result + result + header_key + ": " + header_val + "\n"

        return result

    def __init__(self, format_template: str = None):
        self._template = None
        if format_template is None:
            format_template = self.debug()
        self._template = format_template

    def format(self, response: Response, error=None):
        url_scheme, url_auth, url_host, url_port, url_path, url_query, url_fragment = parse_url(response.url)

        request_val_headers = ""
        for request_header_key, request_header_val in response.request.headers.items():
            request_val_headers += "\n{" + request_header_key + "}: " + request_header_val

        request_val = "".join(filter(None, [
            response.request.method,
            " ",
            url_path,
            url_query,
            " HTTP/?",
            "\nHost: ",
            url_host,
            request_val_headers,
            "\n\n",
            response.request.body.decode(),
        ]))

        response_val_headers = ""
        for response_header_key, response_header_val in response.headers.items():
            response_val_headers += "\n{" + response_header_key + "}: " + response_header_val

        response_val = "".join(filter(None, [
            "HTTP/? ",
            str(response.status_code),
            " ",
            response.reason,
            response_val_headers,
            "\n\n",
            response.content.decode(),
        ]))

        req_headers = "".join(filter(None, [
            response.request.method,
            " ",
            url_path,
            url_query,
            " HTTP/?\n",
            self.headers(response.request.headers),
        ]))

        res_headers = "".join(filter(None, [
            "HTTP/? ",
            str(response.status_code),
            " ",
            response.reason,
            self.headers(response.headers),
        ]))

        req_header_user_agent = response.request.headers.get('User-Agent') or ""
        res_header_content_length = response.headers.get('Content-Length') or ""
        req_body = response.request.body.decode() or ""
        res_body = response.content.decode() or ""
        utc_now = datetime.utcnow().isoformat()
        date_common_log = datetime.now().__format__('%d/%m/%Y:%H:%M:%S %Z')
        method = response.request.method or ""
        version = '?'

        result_dict = {
            'request': request_val,
            'response': response_val,
            'req_headers': req_headers,
            'res_headers': res_headers,
            'req_header_User-Agent': req_header_user_agent,
            'res_header_Content-Length': res_header_content_length,
            'req_body': req_body,
            'res_body': res_body,
            'ts': utc_now,
            'date_iso_8601': utc_now,
            'date_common_log': date_common_log,
            'method': method,
            'version': version,
            'uri': response.url,
            'url': response.url,
            'target': response.url,
            'req_version': '?',
            'res_version': '?',
            'host': url_host,
            'hostname': socket.gethostname(),
            'code': str(response.status_code),
            'phrase': response.reason,
            'error': error
        }
        message = self._template.format(**result_dict)

        redacted = "\\1REDACTED\\3"
        replacements = [
            "password",
            "accountnumber",
            "cardnum",
            "ssn",
            "achaccountnumber",
            "wireaccountnumber",
            "taxid",
            "sessionid",
        ]
        for replacement in replacements:
            message = re.sub(r"(<" + replacement + "[^>]*>)(.*?)(</" + replacement + ">)", redacted, message,
                             flags=re.IGNORECASE)

        return message
