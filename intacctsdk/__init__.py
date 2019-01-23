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

from .version import __version__

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

# ... Clean up.
del NullHandler

from .configs import ClientConfig, RequestConfig
from .clients import OnlineClient, OfflineClient, SessionProvider
from .exceptions import IntacctException, ResponseException, ResultException
from .logs import MessageFormatter
from .xml_requests import RequestBlock
from .xml_responses import OnlineResponse, OfflineResponse

from . import functions
