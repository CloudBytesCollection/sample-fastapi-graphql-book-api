from __future__ import annotations

from typing import Optional

import strawberry
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from src.models.authors.author_models import Author


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class Book:
    _id: strawberry.ID
    title: str
    author: Author
    price: float
    subtitle: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    book_format: Optional[str] = None
    rating: Optional[float] = None
    async_update_required: Optional[bool] = False
    created_on: Optional[str] = None
    last_updated_on: Optional[str] = None

    @property
    def id(self) -> strawberry.ID:
        """Decorator used to create getters and setters for a unique identifier."""
        return self._id
