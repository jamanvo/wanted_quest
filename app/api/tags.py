from fastapi import APIRouter, Depends

from app.schemas.companies import CompanyDetail
from app.services.common import get_language

router = APIRouter()


@router.get(
    "/",
    response_model=list[CompanyDetail],
    dependencies=[Depends(get_language)],
)
def search_company_from_tag(query: str):
    return
