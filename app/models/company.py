import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    tags = relationship("CompanyTag", back_populates="company", order_by="CompanyTag.id")
    localized_names = relationship("CompanyLocalizedName", back_populates="company")
    name_tokens = relationship("CompanyNameToken", back_populates="company")


class CompanyLocalizedName(Base):
    __tablename__ = "company_localized_names"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String)
    language = Column(String)

    company = relationship("Company", back_populates="localized_names")

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

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    tokenized_name = Column(String)

    company = relationship("Company", back_populates="name_tokens")

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "company_id",
            "tokenized_name",
            name="unique_company_name_tokens_company_id_name_tokenized_name",
        ),
    )


class CompanyTag(Base):
    __tablename__ = "company_tags"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    tag_origin_id = Column(Integer, ForeignKey("tag_origins.id"), nullable=False)
    tag = Column(String)
    language = Column(String)

    company = relationship("Company", back_populates="tags")

    __table_args__ = (
        sqlalchemy.UniqueConstraint(
            "company_id",
            "tag",
            "language",
            name="unique_company_tags_company_id_tag_language",
        ),
    )
