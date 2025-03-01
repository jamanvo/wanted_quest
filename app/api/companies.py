from fastapi import APIRouter

from app.schemas.companies import CompanyDetail, CompanyCreateBody

router = APIRouter()


@router.get("/{company_name}", response_model=CompanyDetail)
def get_company(company_name: str):
    return


@router.post("/", response_model=CompanyDetail)
def create_company(body: CompanyCreateBody):
    return


@router.delete("/{company_name}/tags/{tag}", response_model=CompanyDetail)
def delete_tag(company_name: str, tag: str):
    return
