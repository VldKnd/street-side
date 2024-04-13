import functools
import hashlib
import typing
from typing import Any, Dict

import orjson
import pydantic
import pydantic.config


def tuple_default(obj):
    if isinstance(obj, (tuple,)):
        return tuple(obj)


def sorted_orjson_dumps(v: typing.Any, *, default: typing.Any) -> str:
    """
    Return a json string of a python object.

    It is a wrapper around `orjson.dumps` with the `OPT_SORT_KEYS` to ensure that
    the keys of a dictionary are always sorted.

    Parameters
    ----------
    v : typing.Any
        The object to serialize.
    default : typing.Any
        The default function to use.

    Returns
    -------
    str
        The JSON representation of the object.
    """

    return orjson.dumps(
        v,
        option=orjson.OPT_SORT_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        default=default,
    ).decode("utf-8")


def str_hash(s: str) -> str:
    """
    Return a hash of the string object passed in.
    This function is generic but is used, in the context of this repo,
    for the definition of a unique identifier of specific data models.
    It is not exactly unique however the "sha256" function is very unlikely to yield collisions.
    This identifier is used to identify a data model in a database.
    In a SQL database, this identifier is of type `VARCHAR(64)`.

    Parameters
    ----------
    s : str
        The string to hash.
    Returns
    -------
    str
        The hash of the JSON representation of the object.
        It is a 64 character string.
    """
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

class BaseModelWithHashId(pydantic.BaseModel):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, pydantic.BaseModel):
            self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
            other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__

            return (
                self_type == other_type
                and all(
                    getattr(self, field) == getattr(other, field) for field in self.model_fields
                )
                and self.__pydantic_private__ == other.__pydantic_private__
                and self.__pydantic_extra__ == other.__pydantic_extra__
            )
        else:
            return NotImplemented


    def dict(self, **kwargs) -> Dict[str, Any]:
        """
        Return a dictionary representation of the object.

        Returns
        -------
        Dict[str, Any]
            The dictionary representation of the object.

        Raises
        ------
        ValueError
            If keyword arguments are passed in.
        """
        if kwargs:
            raise ValueError("Keyword arguments are not supported.")

        return self.model_dump()

    @functools.cached_property
    def hash_id(self) -> str:
        """
        Return the hash of the JSON representation of the object.
        It is a 64 character string.

        Returns
        -------
        str
            The hash of the JSON representation of the object.
        """
        # Here we use model_dump() instead of model_dump_json() because
        # model_dump_json() does not yet support keys sorting.
        # Ideally, we would use model_dump_json(sort_keys=True) but this is not yet supported.
        # See, https://github.com/pydantic/pydantic/issues/7424
        obj = self.model_dump()
        json_str = sorted_orjson_dumps(obj, default=tuple_default)
        return str_hash(json_str)
