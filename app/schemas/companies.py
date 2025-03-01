from pydantic import BaseModel

from app.schemas.common import LanguageModel
from app.schemas.tags import TagModel


class CompanyName(BaseModel):
    company_name: str


class CompanyDetail(BaseModel):
    company_name: str
    tags: list[str]


class CompanyCreateBody(BaseModel):
    company_name: LanguageModel
    tags: list[TagModel]
