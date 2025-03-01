from typing import Optional

from pydantic import BaseModel, ConfigDict


class LanguageModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    ko: Optional[str] = None
    en: Optional[str] = None
    jp: Optional[str] = None
