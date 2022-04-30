from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json, LetterCase
import strawberry


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class Review:
    _id: strawberry.ID
    book_id: str
    reviewer_id: str
    rating: float
    review_comments: str
    created_on: datetime = None
    last_updated_on: Optional[datetime] = None

    @property
    def id(self) -> strawberry.ID:
        """Decorator used to create getters and setters for a unique identifier."""
        return self._id
