from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.companies import CompanyDetail, CompanyCreateBody
from app.services.common import get_language
from app.services.company import CompanyCRUDService

router = APIRouter()


@router.get(
    "/{company_name}",
    response_model=CompanyDetail,
)
def get_company(company_name: str, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = CompanyCRUDService(db, language).get(company_name)
    return data


@router.post("/", response_model=CompanyDetail)
def create_company(body: CompanyCreateBody):
    return


@router.delete("/{company_name}/tags/{tag}", response_model=CompanyDetail)
def delete_tag(company_name: str, tag: str):
    return
