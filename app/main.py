from fastapi import FastAPI

from app.api import companies

app = FastAPI(title="Wanted Quest")

app.include_router(companies.router, prefix="/companies", tags=["companies"])
