"""
This module contains a custom formatter that outputs logs as json strings.
This is useful for logging to a file or a stream that can be parsed by
a log aggregator like loki, logstash, etc.
Example
-------
import logging
import sys
from stages_common.jsonlog.formatter import DEFAULT_JSON_FORMATTER
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(DEFAULT_JSON_FORMATTER)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info("Hello world!")
"""

import datetime
import logging
import traceback
from typing import Iterable, List, Mapping, Optional

from uvicorn.logging import AccessFormatter

from street_side_api.app.logging.serializer import DefaultSerializer, Serializer


class Formatter(logging.Formatter):
    """
    Convenience formatter to output logs as json strings.
    """

    serializer: Serializer
    fields_mapping: Mapping[str, str]
    wanted_keys: Optional[List[str]]

    def __init__(
        self,
        serializer: Optional[Serializer],
        fields_mapping: Optional[Mapping[str, str]] = None,
        wanted_keys: Optional[Iterable[str]] = None,
    ):
        """
        Initializes the formatter.
        """
        self.serializer = serializer or DefaultSerializer()
        self.fields_mapping = {**(fields_mapping or {"asctime": "timestamp"})}
        self.wanted_keys = list(wanted_keys) if wanted_keys else []

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record and serializes to json.
        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.
        Returns
        -------
        str
            The formatted log record.
        """

        # format the record message
        record.message = record.getMessage()

        data = vars(record)

        # Add traceback if exception has been raised
        if data.get("exc_info") is not None:
            data["traceback"] = ''.join(
                traceback.format_exception(*data.pop("exc_info"))
            ).splitlines()

        # created is a float timestamp, converts it to a datetime
        data["asctime"] = datetime.datetime.fromtimestamp(data["created"])

        # Filter out unwanted keys
        data = {
            self.fields_mapping.get(k, k): v
            for k, v in data.items()
            if self.fields_mapping.get(k, k) in (self.wanted_keys or data.keys())
        }

        return self.serializer.serialize(data)


API_JSON_FORMATTER = Formatter(
    serializer=DefaultSerializer(),
    fields_mapping={
        "asctime": "timestamp",
    },
    wanted_keys=[
        "filename",
        "levelprefix",
        "client_addr",
        "client_port",
        "request_line",
        "status_code",
        "funcName",
        "levelname",
        "name",
        "message",
        "module",
        "pathname",
        "traceback",
        "timestamp",
    ],
)


class UvicornAccessFormatter(AccessFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_formatter = API_JSON_FORMATTER

    def format(self, record: logging.LogRecord):
        return self.json_formatter.format(record)
