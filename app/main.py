from fastapi import FastAPI

from app.api import companies, tags, search

app = FastAPI(title="Wanted Quest")

app.include_router(companies.router, prefix="/companies", tags=["companies"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(search.router, prefix="/search", tags=["search"])
