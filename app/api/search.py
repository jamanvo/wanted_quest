from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.companies import CompanyName
from app.services.common import get_language
from app.services.company_read import AutoCompleteService

router = APIRouter()


@router.get(
    "/",
    response_model=list[CompanyName],
)
def autocomplete_company_name(query: str, db: Session = Depends(get_db), language: str = Depends(get_language)):
    data = AutoCompleteService(db, language).search(query)
    return data
