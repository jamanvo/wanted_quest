from typing import Annotated

from fastapi import Header


def get_language(x_wanted_language: Annotated[str | None, Header(convert_underscores=True)] = "ko"):
    return x_wanted_language
