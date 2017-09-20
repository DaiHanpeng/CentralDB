from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,ResultFlagTable

class ResultFlagInterface():
    """
    db interface for result flag table.
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

    def add_new_record(self,code = None,rid = None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.add(ResultFlagTable(code = code,rid=rid))

    def add_new_records(self, result_list):
        if isinstance(result_list, list):
            for item in result_list:
                if isinstance(item,ResultFlagTable):
                    self.add_new_record(code=item.code,rid=item.rid)
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

    db_interface = ResultFlagInterface()
    # insert normal data
    print 'normal testing:'
    db_interface.add_new_record(code='waived')
    db_interface.add_new_record(code='hello')
    db_interface.add_new_record(code='test',rid=228931)
    db_interface.write_to_db()
    # test insert abnormal data
    # should fail because the foreign key constrain
    print 'abnormal testing:'
    try:
        db_interface.add_new_record(code='test',rid=1122334455)
        db_interface.write_to_db()
    except Exception as e:
        print e

if __name__ == '__main__':
    mytest01()