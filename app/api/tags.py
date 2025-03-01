from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.companies import CompanyDetail
from app.services.common import get_language
from app.services.company_read import CompanySearchService

router = APIRouter()


@router.get("/", response_model=list[CompanyDetail])
def search_company_from_tag(query: str, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = CompanySearchService(db, language).by_tag(query)
    return data
