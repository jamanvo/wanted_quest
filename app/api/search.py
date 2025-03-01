from fastapi import APIRouter

from app.schemas.companies import CompanyDetail

router = APIRouter()


@router.get("/", response_model=list[CompanyDetail])
def autocomplete_company_name(query: str):
    return
