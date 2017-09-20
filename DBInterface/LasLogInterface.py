from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,LasLogTable

class LasLogInterface():
    """
    db interface for las_log table.
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

    def update_record(self, \
                      node_id=None, \
                      sample_id=None, \
                      carrier_id=None, \
                      timestamp=None, \
                      node_type=None, \
                      log_code=None, \
                      need_deliver=None, \
                      delivered=None, \
                      delivered_time_stamp=None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.merge(LasLogTable(node_id=node_id, \
                                       sample_id=sample_id, \
                                       carrier_id=carrier_id, \
                                       timestamp=timestamp, \
                                       node_type=node_type, \
                                       log_code=log_code, \
                                       need_deliver=need_deliver, \
                                       delivered=delivered, \
                                       delivered_time_stamp=delivered_time_stamp))
        self.write_to_db()

    def update_records(self, las_log_list):
        if isinstance(las_log_list, list) and las_log_list is not None:
            for item in las_log_list:
                if isinstance(item,LasLogTable):
                    self.update_record(node_id=item.node_id, \
                                                   sample_id=item.sample_id, \
                                                   carrier_id=item.carrier_id, \
                                                   timestamp=item.timestamp, \
                                                   node_type=item.node_type, \
                                                   log_code=item.log_code, \
                                                   need_deliver=item.need_deliver, \
                                                   delivered=item.delivered, \
                                                   delivered_time_stamp=item.delivered_time_stamp)
            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex

def test001():
    from datetime import datetime
    db_interface = LasLogInterface()
    db_interface.update_record(node_id='003', node_type='A24', sample_id='test0011',log_code='3044',timestamp=datetime.now())
    #db_interface.update_record(22334455)
    db_interface.write_to_db()

if __name__ == '__main__':
    test001()