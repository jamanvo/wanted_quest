import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)


class CompanyLocalizedName(Base):
    __tablename__ = "company_localized_names"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "company_id",
            "name",
            "language",
            name="unique_company_localized_name_company_id_name_language",
        ),
    )


class CompanyNameToken(Base):
    __tablename__ = "company_name_tokens"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    tokenized_name = Column(String)

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "company_id",
            "tokenized_name",
            name="unique_company_name_tokens_company_id_name_tokenized_name",
        ),
    )


class CompanyTag(Base):
    __tablename__ = "company_tags"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    language = Column(String)

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "company_id",
            "tag",
            "language",
            name="unique_company_tags_company_id_tag_language",
        ),
    )
