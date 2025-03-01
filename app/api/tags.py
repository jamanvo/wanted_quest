from fastapi import APIRouter

from app.schemas.companies import CompanyDetail

router = APIRouter()


@router.get("/", response_model=list[CompanyDetail])
def search_company_from_tag(query: str):
    return
