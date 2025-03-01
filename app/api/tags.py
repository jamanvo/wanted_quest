from fastapi import APIRouter

from app.schemas.tags import SearchCompanyResponse

router = APIRouter()


@router.get("/", response_model=list[SearchCompanyResponse])
def search_company_from_tag(query: str):
    pass
