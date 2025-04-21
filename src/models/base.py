from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from typing import Annotated


str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}
