from fastapi import APIRouter, Depends

from app.schemas.companies import CompanyDetail, CompanyCreateBody
from app.services.common import get_language

router = APIRouter()


@router.get(
    "/{company_name}",
    response_model=CompanyDetail,
)
def get_company(company_name: str, language: str = Depends(get_language)):
    return


@router.post("/", response_model=CompanyDetail)
def create_company(body: CompanyCreateBody):
    return


@router.delete("/{company_name}/tags/{tag}", response_model=CompanyDetail)
def delete_tag(company_name: str, tag: str):
    return
