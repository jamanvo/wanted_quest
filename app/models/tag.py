from sqlalchemy import Column, Integer, ForeignKey, String

from app.database import Base


class TagOrigin(Base):
    __tablename__ = "tag_origins"

    id = Column(Integer, primary_key=True)


class TagValue(Base):
    __tablename__ = "tag_values"

    id = Column(Integer, primary_key=True)
    tag_origin_id = Column(Integer, ForeignKey("tag_origins.id"), nullable=False)
    value = Column(String)
