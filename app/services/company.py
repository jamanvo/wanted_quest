from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, distinct
from sqlalchemy.orm import joinedload

from app.models.company import CompanyNameToken, CompanyLocalizedName, Company
from app.schemas.companies import CompanyName, CompanyDetail
from app.services.common import BaseService


class AutoCompleteService(BaseService):
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


class CompanySearchService(BaseService):
    pass


class CompanyCRUDService(BaseService):
    def get(self, company_name: str) -> CompanyDetail:
        company = self._get_from_name(company_name)
        if not company:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        company = self._get_from_name(company_name)
        return self._make_detail(company)

    def _get_from_name(self, company_name: str) -> Company:
        query = (
            select(Company)
            .options(joinedload(Company.localized_names), joinedload(Company.tags))
            .join(CompanyLocalizedName)
            .where(CompanyLocalizedName.name == company_name)
        )
        return self.db.execute(query).scalars().first()

    def _make_detail(self, company: Company) -> CompanyDetail:
        return CompanyDetail(
            company_name=[n.name for n in company.localized_names if n.language == self.language][0],
            tags=[t.tag for t in company.tags if t.language == self.language],
        )


class CompanyLocalizeNameService:
    pass


class CompanyTagService:
    def add(self, company_id: int, tags: list[str]):
        pass

    def remove(self, company_id: int, tag: str):
        pass
