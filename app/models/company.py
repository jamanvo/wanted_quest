from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)


class CompanyTag(Base):
    __tablename__ = "company_tags"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    tag = Column(String)


class CompanyLocalizedName(Base):
    __tablename__ = "company_localized_names"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)


class CompanyNameToken(Base):
    __tablename__ = "company_name_tokens"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True)
    tokenized_name = Column(String)
