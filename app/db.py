import sqlalchemy as sa
from sqlalchemy import orm as orm
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

metadata = sa.MetaData()
Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = 'companies'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employee_count = Column(Integer)

    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    employees = orm.relationship('Employee', back_populates='company')


class Employee(Base):
    __tablename__ = 'employees'

    # Columns
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    name = Column(String)

    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    company = orm.relationship('Company', back_populates='employees', uselist=False)

