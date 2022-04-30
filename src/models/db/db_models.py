from __future__ import annotations

from typing import List
import strawberry
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class BulkRecordUpdateResponse:
    update_responses: List[UpdateRecord]
    error_message: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class GetRecord:
    success: bool
    record_id: str = None
    error_message: str = None
    timestamp: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class CreateRecord:
    success: bool
    record_id: str = None
    error_message: str = None
    timestamp: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class UpdateRecord:
    success: bool
    record_id: str = None
    error_message: str = None
    timestamp: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class DeleteRecord:
    success: bool = None
    record_id: str = None
    error_message: str = None
    timestamp: str = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@strawberry.enum
class DatabaseCollectionTypes(Enum):
    BOOKS = "books"
    REVIEWS = "reviews"
