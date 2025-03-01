from pydantic import BaseModel


class SearchCompanyResponse(BaseModel):
    company_name: str
