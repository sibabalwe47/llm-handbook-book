from abc import ABC
from typing import Optional
from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory

class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"