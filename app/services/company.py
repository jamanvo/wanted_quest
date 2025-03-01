import re
from typing import Sequence

from sqlalchemy import select, distinct
from sqlalchemy.orm import Session

from app.models.company import CompanyNameToken, CompanyLocalizedName
from app.schemas.companies import CompanyName


class CompanySearchService:
    def __init__(self, db: Session, language: str):
        self.db = db
        self.language = language

    def search(self, keyword: str) -> list[CompanyName]:
        company_ids = self._get_company_ids(keyword)
        company_names = self._get_company_names(company_ids)

        return [CompanyName(company_name=cn) for cn in company_names]

    def _get_company_ids(self, keyword: str) -> Sequence[int]:
        query = select(distinct(CompanyNameToken.company_id)).where(CompanyNameToken.tokenized_name == keyword)
        return self.db.execute(query).scalars().all()

    def _get_company_names(self, company_ids: Sequence[int]) -> Sequence[str]:
        query = (
            select(CompanyLocalizedName.name)
            .where(
                CompanyLocalizedName.company_id.in_(company_ids),
                CompanyLocalizedName.language == self.language,
            )
            .order_by(CompanyLocalizedName.id.asc())
        )
        return self.db.execute(query).scalars().all()


class CompanyCRUDService:
    pass


class TokenizeService:
    @staticmethod
    def tokenize_name(name: str) -> list[str]:
        target_name = re.sub(r"\s|\(.*\)|\(|\)|주식회사|inc\.", "", name.lower())
        max_length = len(target_name)

        result = []
        for i in range(2, max_length + 1):
            for j in range(len(target_name)):
                token = target_name[j : j + i]

                if len(token) == i:
                    result.append(token)
                elif len(token) < i:
                    break

        return result


class CompanyLocalizeNameService:
    pass


class CompanyTagService:
    def add(self, company_id: int, tags: list[str]):
        pass

    def remove(self, company_id: int, tag: str):
        pass
