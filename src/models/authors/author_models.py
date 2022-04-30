from __future__ import annotations

from typing import Optional

import strawberry
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
@strawberry.type
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None  # Note the optional middle name


# Inputs have to be defined separately if used in resolvers
@strawberry.input
class AuthorInput:
    first_name: str
    last_name: str
    middle_name: str = None
