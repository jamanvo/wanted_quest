from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models import CompanyTag
from app.models.tag import TagValue
from app.schemas.tags import TagModel
from app.services.common import BaseService, CommonCompanyGetService, CommonCompanyInfoService, CommonTagCreateService


class CompanyTagService(BaseService):
    def __init__(self, db: Session, language: str):
        super().__init__(db, language)
        self._company_info_service = CommonCompanyInfoService(self.language)
        self._company_get_service = CommonCompanyGetService(self.db)
        self._tag_create_service = CommonTagCreateService(self.db)

    def add(self, company_name: str, tags: list[TagModel]):
        company = self._company_get_service.get_from_name(company_name)

        self._tag_create_service.create_tags(company.id, tags)

        return self._company_info_service.make_detail(company)

    def remove(self, company_name: str, tag: str):
        company = self._company_get_service.get_from_name(company_name)
        tag_origin_id = self._get_tag_origin_id(tag)

        self._delete_company_tag(company.id, tag_origin_id)

        self.db.refresh(company)
        return self._company_info_service.make_detail(company)

    def _get_tag_origin_id(self, tag: str) -> int | None:
        query = select(TagValue.tag_origin_id).where(TagValue.value == tag)
        if result := self.db.execute(query).scalar_one_or_none():
            return result

    def _delete_company_tag(self, company_id: int, tag_origin_id: int | None) -> None:
        if not tag_origin_id:
            return

        query = delete(CompanyTag).where(
            CompanyTag.company_id == company_id,
            CompanyTag.tag_origin_id == tag_origin_id,
        )
        self.db.execute(query)
        self.db.commit()
