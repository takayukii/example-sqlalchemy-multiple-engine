import sqlalchemy as sa
from sqlalchemy import orm as orm
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

metadata = sa.MetaData()
Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_count = Column(Integer)

    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    name = Column(String)

    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())


def setup_relationships(company_class, employee_class):
    company_class.employees = orm.relationship(employee_class.__name__, back_populates='company')
    employee_class.company = orm.relationship(company_class.__name__, back_populates='employees', uselist=False)
