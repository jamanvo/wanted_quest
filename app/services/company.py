from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, distinct, exists
from sqlalchemy.orm import joinedload, Session

from app.models.company import CompanyNameToken, CompanyLocalizedName, Company, CompanyTag
from app.schemas.common import LanguageModel
from app.schemas.companies import CompanyName, CompanyDetail, CompanyCreateBody
from app.schemas.tags import TagModel
from app.services.common import BaseService, CompanyInfoService
from app.services.tokenizer import TokenizeService


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
    def __init__(self, db: Session, language: str):
        super().__init__(db, language)
        self._company_info_service = CompanyInfoService

    def get(self, company_name: str) -> CompanyDetail:
        company = self._get_from_name(company_name)
        if not company:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        company = self._get_from_name(company_name)
        return self._company_info_service.make_detail(company, self.language)

    def _get_from_name(self, company_name: str) -> Company:
        query = (
            select(Company)
            .options(joinedload(Company.localized_names), joinedload(Company.tags))
            .join(CompanyLocalizedName)
            .where(CompanyLocalizedName.name == company_name)
        )
        return self.db.execute(query).scalars().first()


class CompanyCreateService(BaseService):
    def __init__(self, db: Session, language: str):
        super().__init__(db, language)
        self._company_info_service = CompanyInfoService
        self._tokenize_service = TokenizeService

    def create(self, body: CompanyCreateBody):
        print(1)
        if self._check_duplicate(body.company_name):
            print(2)
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        # create company
        company = self._create_company()
        print(3, company)
        # create name
        self._create_names(company.id, body.company_name)
        print(4)
        # create tag
        self._create_tags(company.id, body.tags)
        print(5)

        self.db.commit()
        print(6)

        return self._company_info_service.make_detail(company, self.language)

    def _check_duplicate(self, company_names: LanguageModel) -> bool:
        query = None
        for k, v in company_names.model_dump().items():
            if not v:
                continue

            query = select(
                exists().where(
                    CompanyLocalizedName.name == v,
                    CompanyLocalizedName.language == k,
                )
            )
            break

        if query is None:
            return True

        print(query)
        print(self.db.execute(query).scalar())
        return self.db.execute(query).scalar()

    def _create_company(self) -> Company:
        company = Company()
        self.db.add(company)
        self.db.flush()

        return company

    def _create_names(self, company_id: int, company_names: LanguageModel) -> None:
        for k, v in company_names.model_dump().items():
            if not v:
                continue

            name = CompanyLocalizedName(company_id=company_id, name=v, language=k)
            self.db.add(name)

            # tokenize
            for t_name in self._tokenize_service.tokenize_name(v):
                token_name = CompanyNameToken(company_id=company_id, tokenized_name=t_name)
                self.db.add(token_name)

    def _create_tags(self, company_id: int, tags: list[TagModel]) -> None:
        for tag in tags:
            tag_names = tag.tag_name

            for k, v in tag_names.model_dump().items():
                if not v:
                    continue

                t = CompanyTag(company_id=company_id, tag=v, language=k)
                self.db.add(t)


class CompanyTagService:
    def add(self, company_id: int, tags: list[str]):
        pass

    def remove(self, company_id: int, tag: str):
        pass
