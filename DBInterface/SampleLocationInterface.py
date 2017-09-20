from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,SampleLocationTable

class SampleLocationInterface():
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

    def add_new_record(self, sid, location=None, timestamp=None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead of add() to avoid duplicated insert error from MySQL.
        self.session.merge(SampleLocationTable(sid,location,timestamp))

    def add_new_records(self, sample_location_list):
        if isinstance(sample_location_list, list):
            for item in sample_location_list:
                if isinstance(item,SampleLocationTable):
                    self.add_new_record(item.sid,item.location,item.timestamp)
                else:
                    print 'sample location type error!'
            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex


def mytest01():
    from datetime import datetime
    db_interface = SampleLocationInterface()
    # insert normal data
    print 'normal testing:'
    db_interface.add_new_record('test001','IOM',datetime.now())
    db_interface.add_new_record('test002','RSM',datetime.now())
    # test insert abnormal data
    # should fail because the foreign key constrain
    #print 'abnormal testing:'
    #db_interface.add_new_record('test003','03','Urine','undefined_pid')
    db_interface.write_to_db()



if __name__ == '__main__':
    mytest01()