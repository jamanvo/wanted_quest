from pydantic import BaseModel, ConfigDict


class LanguageModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    ko: str | None
    en: str | None
    jp: str | None
