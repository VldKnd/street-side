from pydantic import BaseModel


class Name(BaseModel):
    """
    Name of a street-side object.
    """
    name: str