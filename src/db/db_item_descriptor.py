from dataclasses import dataclass
import datetime
from typing import Any, Self


@dataclass(kw_only=True)
class DbItemDescriptor:
    """
    Dataclass that holds extra fields that are spcific to the
    Product when stored as a row in the database, such as ID and datestamps
    """

    ID: int
    Type: str
    CreatedAt: datetime.datetime
    LastUpdatedAt: datetime.datetime

    @classmethod
    def create_from_dict(cls, dict: dict[str, Any]) -> Self:
        """
        Factory method for creating a ProductDescriptor from a dictionary.
        """

        descriptor = cls(
            ID=dict["ID"],
            Type=dict["Type"],
            CreatedAt=dict["CreatedAt"],
            LastUpdatedAt=dict["LastUpdatedAt"],
        )
        return descriptor
