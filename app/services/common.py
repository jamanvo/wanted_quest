from typing import Annotated

from fastapi import Header
from sqlalchemy.orm import Session


def get_language(x_wanted_language: Annotated[str | None, Header(convert_underscores=True)] = "ko"):
    return x_wanted_language


class BaseService:
    def __init__(self, db: Session, language: str):
        self.db = db
        self.language = language
