from sqlalchemy import event
from sqlalchemy.exc import InvalidRequestError

from app import db


class ListenersRegisterer:

    def __init__(self, sessionmaker):
        self.Session = sessionmaker

    def up(self):
        try:
            # Prevent duplicated registration
            self.down()
        except InvalidRequestError as ex:
            pass

        event.listen(db.Employee, 'after_insert', self.__after_insert)

    def down(self):
        event.remove(db.Employee, 'after_insert', self.__after_insert)

    def __after_insert(self, mapper, connection, target):
        print('__after_insert: employee.name = {}'.format(target.name))
        session = self.Session(bind=connection)

        company = session.query(db.Company).filter_by(id=target.company_id).first()
        company.employee_count = session.query(db.Employee).filter_by(company_id=target.company_id).count()

        session.commit()
        session.close()
