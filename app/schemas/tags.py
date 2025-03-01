from pydantic import BaseModel

from app.schemas.common import LanguageModel


class TagModel(BaseModel):
    tag_name: LanguageModel
