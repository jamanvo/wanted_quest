from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.companies import CompanyDetail, CompanyCreateBody
from app.schemas.tags import TagModel
from app.services.common import get_language
from app.services.company_create import CompanyCreateService
from app.services.company_read import CompanySearchService
from app.services.tag import CompanyTagService

router = APIRouter()


@router.get(
    "/{company_name}",
    response_model=CompanyDetail,
)
def get_company(company_name: str, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = CompanySearchService(db, language).by_name(company_name)
    return data


@router.post("/", response_model=CompanyDetail)
def create_company(body: CompanyCreateBody, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = CompanyCreateService(db, language).create(body)
    return data


@router.put("/{company_name}/tags", response_model=CompanyDetail)
def add_tags(
    company_name: str,
    body: list[TagModel],
    db: Session = Depends(get_db),
    language: str = Depends(get_language),
):
    data = CompanyTagService(db, language).add(company_name, body)
    return data


@router.delete("/{company_name}/tags/{tag}", response_model=CompanyDetail)
def remove_tag(company_name: str, tag: str, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = CompanyTagService(db, language).remove(company_name, tag)
    return data
