import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from app import db, listener_registers

try:
    os.unlink('sqlite1.db')
    os.unlink('sqlite2.db')
except Exception as ex:
    pass


Company1 = type('Company1', (db.Company,), {})
Employee1 = type('Employee1', (db.Employee,), {})
db.setup_relationships(company_class=Company1, employee_class=Employee1)

engine1 = sqlalchemy.create_engine('sqlite:///sqlite1.db', echo=False)
db.metadata.bind = engine1
db.Base.metadata.create_all()
db.metadata.bind = None
Session1 = sessionmaker()
Session1.configure(bind=engine1, expire_on_commit=False, autoflush=False)
session1 = Session1()

Company2 = type('Company2', (db.Company,), {})
Employee2 = type('Employee2', (db.Employee,), {})
db.setup_relationships(company_class=Company2, employee_class=Employee2)

engine2 = sqlalchemy.create_engine('sqlite:///sqlite2.db', echo=False)
db.metadata.bind = engine2
db.Base.metadata.create_all()
db.metadata.bind = None
Session2 = sessionmaker()
Session2.configure(bind=engine2, expire_on_commit=False, autoflush=False)
session2 = Session2()

registerer1 = listener_registers.ListenersRegisterer(sessionmaker=Session1, employee_class=Employee1)
registerer1.up()

comppany1_1 = Company1(name='company1_1')
session1.add(comppany1_1)
comppany1_1.employees = [
    Employee1(name='employee1_1'),
    Employee1(name='employee1_2'),
]
session1.commit()
comppany1_1 = session1.query(db.Company).filter_by(name='company1_1').first()
print('company.employee_count = {}'.format(comppany1_1.employee_count))

comppany2_1 = Company2(name='company2_1')
session2.add(comppany2_1)
comppany2_1.employees = [
    Employee2(name='employee2_1'),
    Employee2(name='employee2_2'),
]
session2.commit()
comppany2_1 = session2.query(db.Company).filter_by(name='company2_1').first()
print('company.employee_count = {}'.format(comppany2_1.employee_count))
