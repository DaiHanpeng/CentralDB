from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,ResultTable

class ResultInterface():
    """
    db interface for result table.
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

    def add_new_record(self,\
                       test_name = None,\
                       dilution_profile = None,\
                       dilution_factor = None,\
                       result = None,\
                       datetime = None,\
                       instrument_id = None,\
                       sid = None,\
                       aspect = None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.add(ResultTable(test_name = test_name,\
                                       dilution_profile=dilution_profile,\
                                       dilution_factor= dilution_factor,\
                                       result=result,\
                                       datetime=datetime,\
                                       instrument_id=instrument_id,\
                                       sid=sid,\
                                       aspect = aspect))

    def add_new_records(self,patient_list):
        if isinstance(patient_list,list):
            for item in patient_list:
                if isinstance(item,ResultTable):
                    self.add_new_record(test_name=item.test_name,\
                                        dilution_profile=item.dilution_profile,\
                                        dilution_factor=item.dilution_factor,\
                                        result=item.result,\
                                        datetime=item.datetime,\
                                        instrument_id = item.instrument_id,\
                                        sid=item.sid,\
                                        aspect=item.aspect)
            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex


def test01():
    from datetime import datetime

    db_interface = ResultInterface()
    # insert normal data
    print 'normal testing:'
    db_interface.add_new_record(test_name='Alb',result='12.3',datetime=datetime.now(),sid='test001')
    db_interface.add_new_record(test_name='Alb',result='12.3')
    db_interface.write_to_db()
    # test insert abnormal data
    # should fail because the foreign key constrain
    print 'abnormal testing:'
    db_interface.add_new_record(test_name='Alb',result='12.3',datetime=datetime.now(),sid='undefined_sid')
    db_interface.write_to_db()

if __name__ == '__main__':
    test01()