from fastapi import HTTPException
from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from starlette import status

from app.models.company import CompanyLocalizedName, Company, CompanyNameToken, CompanyTag
from app.schemas.common import LanguageModel
from app.schemas.companies import CompanyCreateBody
from app.schemas.tags import TagModel
from app.services.common import BaseService, CommonCompanyInfoService, CommonTagCreateService
from app.services.tokenizer import TokenizeService


class CompanyCreateService(BaseService):
    def __init__(self, db: Session, language: str):
        super().__init__(db, language)
        self._company_info_service = CommonCompanyInfoService(self.language)
        self._tokenize_service = TokenizeService
        self._tag_create_service = CommonTagCreateService(self.db)

    def create(self, body: CompanyCreateBody):
        if self._check_duplicate(body.company_name):
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

        # create company
        company = self._create_company()
        # create name
        self._create_names(company.id, body.company_name)
        # create tag
        self._tag_create_service.create_tags(company.id, body.tags)

        self.db.commit()

        return self._company_info_service.make_detail(
            company,
        )

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
