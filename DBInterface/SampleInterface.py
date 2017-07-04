from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,SampleTable

class SampleInterface():
    """
    db interface for sample table.
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

    def add_new_record(self, sid, tube_type=None, sample_type=None, pid=None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.merge(SampleTable(sid,tube_type,sample_type,pid))

    def add_new_records(self,patient_list):
        if isinstance(patient_list,list):
            for item in patient_list:
                if isinstance(item,SampleTable):
                    self.add_new_record(item.sid,item.tube_type,item.sample_type,item.pid)
            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex


def test01():
    db_interface = SampleInterface()
    # insert normal data
    print 'normal testing:'
    db_interface.add_new_record('test001','03','Serum')
    db_interface.add_new_record('test002','03','Urine','test001')
    # test insert abnormal data
    # should fail because the foreign key constrain
    print 'abnormal testing:'
    db_interface.add_new_record('test003','03','Urine','undefined_pid')
    db_interface.write_to_db()

if __name__ == '__main__':
    test01()