from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, distinct
from sqlalchemy.orm import Session

from app.models.company import CompanyNameToken, CompanyLocalizedName
from app.schemas.companies import CompanyName, CompanyDetail
from app.services.common import BaseService, CommonCompanyInfoService, CommonCompanyGetService


class AutoCompleteService(BaseService):
    def search(self, keyword: str) -> list[CompanyName]:
        company_ids = self._get_company_ids(keyword)
        company_names = self._get_company_names(company_ids)

        return [CompanyName(company_name=cn) for cn in company_names]

    def _get_company_ids(self, keyword: str) -> Sequence[int]:
        query = select(distinct(CompanyNameToken.company_id)).where(CompanyNameToken.tokenized_name == keyword)
        return self.db.execute(query).unique().scalars().all()

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
    def __init__(self, db: Session, language: str):
        super().__init__(db, language)
        self._company_info_service = CommonCompanyInfoService(self.language)
        self._company_get_service = CommonCompanyGetService(self.db)

    def by_name(self, company_name: str) -> CompanyDetail:
        company = self._company_get_service.get_from_name(company_name)
        if not company:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return self._company_info_service.make_detail(company)

    def by_tag(self, tag: str) -> list[CompanyDetail]:
        companies = self._company_get_service.get_from_tag(tag)

        return [self._company_info_service.make_detail(c, False) for c in companies]
