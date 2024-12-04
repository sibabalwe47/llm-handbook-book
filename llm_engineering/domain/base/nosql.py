
import uuid
from abc import ABC
from typing import Generic, Type, TypeVar

from zenml.logger import get_logger
from pydantic import UUID4, BaseModel, Field
from pymongo import errors

logger = get_logger(__name__)


# exceptions
from llm_engineering.domain.exceptions import ImproperlyConfigured

# MongoDB connection
from llm_engineering.infrastructure.db.mongo import connection

# Settings (configuration)
from llm_engineering.settings import settings

# database
_database = connection.get_database(settings.DATABASE_NAME)

T = TypeVar("T", bound="NoSQLBaseDocument")

class NoSQLBaseDocument(BaseModel, Generic[T], ABC):
    """"""

    id: UUID4 = Field(default_factory=uuid.uuid4)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        return self.id == value.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    @classmethod
    def from_mongo(cls: Type[T], data: dict) -> T:
        """Convert "_id" (str object) into "id" (UUID object)."""

        if not data:
            raise ValueError("Data is empty")
        
        id = data.pop("_id")

        return cls(**dict(data, id=id))
    
    def to_mongo(self: Type[T], **kwargs) -> dict:
        """Convert "id" (UUID object) into "_id" (str object)."""
        exclude_unset = kwargs.pop("exclude_unset", False)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(exclude_unset=exclude_unset, by_alias=by_alias, **kwargs)

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))

        for key, value in parsed.items():
            if isinstance(value, uuid.UUID):
                parsed[key] = str(value)

        return parsed

    @classmethod
    def get_or_create(cls: Type[T], **filter_options) -> T:
        """"""
        # Get the collection
        collection = _database[cls.get_collection_name()]

        try:
            instance = collection.find_one(filter_options)

            if instance:
                return cls.from_mongo(instance)
            
            new_instance = cls(**filter_options)
            new_instance = new_instance.save();

        except errors.OperationFailure:
            print(f"Failed to retrieve document with filter options: {filter_options}")

            raise

    @classmethod
    def get_collection_name(cls: Type[T]):
        """"""
        if not hasattr(cls, "Settings") or not hasattr(cls.Settings,"name"):
            raise ImproperlyConfigured(
                "Document should be defined in Settings configuration class with the name of the collection"
            )
        
        return cls.Settings.name
    
    def save(self: T, **kwargs) -> T | None:
        collection = _database[self.get_collection_name()]

        try:
            collection.insert_one(self.to_mongo(**kwargs))
            return self
        except errors.WriteError:
            print("Failed to insert document")
            return None