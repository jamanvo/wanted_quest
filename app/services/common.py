from typing import Annotated

from fastapi import Header
from sqlalchemy.orm import Session

from app.models.company import Company
from app.schemas.companies import CompanyDetail


def get_language(x_wanted_language: Annotated[str | None, Header(convert_underscores=True)] = "ko"):
    return x_wanted_language


class BaseService:
    def __init__(self, db: Session, language: str):
        self.db = db
        self.language = language


class CompanyInfoService:
    @staticmethod
    def make_detail(company: Company, language: str) -> CompanyDetail:
        return CompanyDetail(
            company_name=[n.name for n in company.localized_names if n.language == language][0],
            tags=[t.tag for t in company.tags if t.language == language],
        )
