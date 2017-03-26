import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from app import db, listener_registers

try:
    os.unlink('sqlite1.db')
    os.unlink('sqlite2.db')
except Exception as ex:
    pass

engine1 = sqlalchemy.create_engine('sqlite:///sqlite1.db', echo=False)
db.metadata.bind = engine1
db.Base.metadata.create_all()
db.metadata.bind = None
Session1 = sessionmaker()
Session1.configure(bind=engine1, expire_on_commit=False, autoflush=False)
session1 = Session1()

engine2 = sqlalchemy.create_engine('sqlite:///sqlite2.db', echo=False)
db.metadata.bind = engine2
db.Base.metadata.create_all()
db.metadata.bind = None
Session2 = sessionmaker()
Session2.configure(bind=engine2, expire_on_commit=False, autoflush=False)
session2 = Session2()

registerer1 = listener_registers.ListenersRegisterer(sessionmaker=Session1)
registerer1.up()

comppany1_1 = db.Company(name='company1_1')
session1.add(comppany1_1)
comppany1_1.employees = [
    db.Employee(name='employee1_1'),
    db.Employee(name='employee1_2'),
]
session1.commit()
comppany1_1 = session1.query(db.Company).filter_by(name='company1_1').first()
print('company.employee_count = {}'.format(comppany1_1.employee_count))

comppany2_1 = db.Company(name='company2_1')
session2.add(comppany2_1)
comppany2_1.employees = [
    db.Employee(name='employee2_1'),
    db.Employee(name='employee2_2'),
]
session2.commit()
comppany2_1 = session2.query(db.Company).filter_by(name='company2_1').first()
print('company.employee_count = {}'.format(comppany2_1.employee_count))
