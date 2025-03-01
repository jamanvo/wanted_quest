from fastapi import APIRouter

from app.schemas.tags import SearchCompanyResponse

router = APIRouter()


@router.get("/", response_model=list[SearchCompanyResponse])
@router.get("/")
def autocomplete_company_name(query: str):
    pass
