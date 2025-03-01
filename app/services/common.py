from typing import Annotated, Sequence

from fastapi import Header
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models import TagOrigin
from app.models.company import Company, CompanyLocalizedName, CompanyTag
from app.models.tag import TagValue
from app.schemas.companies import CompanyDetail
from app.schemas.tags import TagModel


def get_language(x_wanted_language: Annotated[str | None, Header(convert_underscores=True)] = "ko"):
    return x_wanted_language


class BaseService:
    def __init__(self, db: Session, language: str):
        self.db = db
        self.language = language


class CommonCompanyInfoService:
    def __init__(self, language: str):
        self.language = language

    def make_detail(self, company: Company, only_language_matched: bool = True) -> CompanyDetail:
        return CompanyDetail(
            company_name=self._get_company_name(company.localized_names, only_language_matched),
            tags=[t.tag for t in company.tags if t.language == self.language],
        )

    def _get_company_name(self, localized_names: list[CompanyLocalizedName], only_language_matched: bool) -> str:
        names = {n.language: n.name for n in localized_names}
        if only_language_matched:
            return names.get(self.language)

        return names[next(iter(names))]


class CommonCompanyGetService:
    def __init__(self, db: Session):
        self.db = db

    def get_from_name(self, company_name: str) -> Company:
        query = (
            select(Company)
            .options(joinedload(Company.localized_names), joinedload(Company.tags))
            .join(CompanyLocalizedName)
            .where(CompanyLocalizedName.name == company_name)
        )

        return self.db.execute(query).scalars().first()

    def get_from_tag(self, tag: str) -> Sequence[Company]:
        query = (
            select(Company)
            .options(joinedload(Company.localized_names), joinedload(Company.tags))
            .join(CompanyTag)
            .where(CompanyTag.tag == tag)
        )

        return self.db.execute(query).unique().scalars().all()


class CommonTagCreateService:
    def __init__(self, db: Session):
        self.db = db

    def create_tags(self, company_id: int, tags: list[TagModel]) -> None:
        for tag in tags:
            tag_names = tag.tag_name
            tag_name_dict = tag_names.model_dump()

            to_id = self._get_or_create_tag_info([t for t in tag_name_dict.values()])
            for k, v in tag_name_dict.items():
                if not v:
                    continue

                t = CompanyTag(company_id=company_id, tag=v, language=k, tag_origin_id=to_id)
                self.db.add(t)
                try:
                    self.db.commit()
                except IntegrityError:
                    self.db.rollback()

    def _get_or_create_tag_info(self, tags: list[str]) -> int:
        query = select(TagValue).where(TagValue.value.in_(tags))
        result = self.db.execute(query).scalar_one_or_none()

        if result:
            return result.tag_origin_id

        to = TagOrigin()
        self.db.add(to)
        self.db.flush()

        for tag in tags:
            tv = TagValue(tag_origin_id=to.id, value=tag)
            self.db.add(tv)

        self.db.commit()

        return to.id
