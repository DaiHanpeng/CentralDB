from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,PatientTable

class PatientInterface():
    """
    db interface for patient table.
    """
    def __init__(self):
        DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/sys_info'

        self.engine = create_engine(DB_CONNECT_STRING,echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

        self.init_database()


    def init_database(self):
        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def add_new_record(self, pid, fname=None, lname=None, birthday=None, sex=None, location=None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.merge(PatientTable(pid,fname,lname,birthday,sex,location))

    def add_new_records(self,patient_list):
        if isinstance(patient_list,list):
            for item in patient_list:
                if isinstance(item,PatientTable):
                    self.add_new_record(item.pid,item.fname,item.lname,item.birthday,item.sex,item.location)
            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex


def test01():
    db_interface = PatientInterface()
    db_interface.add_new_record('test001','dai01','han peng01')
    db_interface.add_new_record(22334455)
    db_interface.write_to_db()

if __name__ == '__main__':
    test01()