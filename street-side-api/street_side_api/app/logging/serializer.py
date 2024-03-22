import datetime
import json
from typing import Any, Protocol

from typing_extensions import runtime_checkable


@runtime_checkable
class Serializer(Protocol):
    def serialize(self, obj: Any) -> str: ...


class DefaultJsonEncoder(json.JSONEncoder):
    """
    Convenience custom encoder extending the default json.JSONEncoder
    This is used to handle datetime objects, exceptions and tracebacks.
    """

    def default(self, obj):
        # handle datetime objects
        if isinstance(obj, datetime.datetime):
            dt = obj.astimezone(datetime.timezone.utc)
            return dt.isoformat(sep='T', timespec='milliseconds')

        # handle other types below if need be...

        else:
            return repr(obj)


class DefaultSerializer:
    def serialize(self, obj: Any) -> str:
        return json.dumps(
            obj,
            sort_keys=True,
            indent=None,
            cls=DefaultJsonEncoder,
        )
