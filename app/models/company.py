from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)


class CompanyTag(Base):
    __tablename__ = "company_tags"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True, index=True)
    Tag = Column(String, index=True)


class CompanyLocalizedName(Base):
    __tablename__ = "company_tags"

    company = relationship("Company", back_populates="items")

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    Tag = Column(String, index=True)
