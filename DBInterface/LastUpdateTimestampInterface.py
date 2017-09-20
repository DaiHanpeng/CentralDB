from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_,or_

from Tables import BaseModel,LastUpdateTimestampTable


class LastUpdateTimestampInterface():
    """
    db interface for table last_update_timestamp
    """
    def __init__(self):
        DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/sys_info'

        #DB_CONNECT_STRING = 'sqlite:///tutorial.db'
        self.engine = create_engine(DB_CONNECT_STRING,echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

        self.init_database()


    def init_database(self):
        #self.session.execute('use tat')

        self.init_tables()
        self.session.commit()

    def init_tables(self):
        BaseModel.metadata.create_all(self.engine)

    def get_log_file_last_update_timestamp(self,type_id):
        update_timestamp = self.session.query(LastUpdateTimestampTable.last_file_update_timestamp).filter_by(type_id=type_id).first()
        if update_timestamp:
            print 'type id: ', type_id, '; get last file updated timestamp: ', update_timestamp.last_file_update_timestamp
            return update_timestamp.last_file_update_timestamp

    def set_log_file_last_update_timestamp(self,type_id,timestamp):
        if not isinstance(timestamp,datetime):
            print 'set_log_file_last_update_timestamp not a datetime object!'
            print type_id
            print timestamp
            return
        if isinstance(type_id,str):
            self.touch_new_record(type_id=type_id)
            query = self.session.query(LastUpdateTimestampTable)
            query.filter(LastUpdateTimestampTable.type_id == type_id).update({LastUpdateTimestampTable.last_file_update_timestamp:timestamp})
            self.write_to_db()
            print 'type id = ', type_id, '; last_file_update_timestamp set to => ', timestamp

    def get_record_last_update_timestamp(self,type_id):
        update_timestamp = self.session.query(LastUpdateTimestampTable.last_record_update_timestamp).filter_by(type_id=type_id).first()
        if update_timestamp:
            print 'type id: ', type_id, '; get last record updated timestamp: ', update_timestamp.last_record_update_timestamp
            return update_timestamp.last_record_update_timestamp

    def set_record_last_update_timestamp(self,type_id,timestamp):
        if not isinstance(timestamp,datetime):
            print 'set_record_last_update_timestamp not a datetime object!'
            print type_id
            print timestamp
            return
        if isinstance(type_id,str):
            self.touch_new_record(type_id=type_id)
            query = self.session.query(LastUpdateTimestampTable)
            query.filter(LastUpdateTimestampTable.type_id == type_id).update({LastUpdateTimestampTable.last_record_update_timestamp:timestamp})
            self.write_to_db()
            print 'type id = ', type_id, 'last_record_update_timestamp set to => ', timestamp

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex

    def touch_new_record(self,type_id):
        if isinstance(type_id,str):
            if len(type_id) > 16:
                type_id = type_id[:16]
            if not self.check_if_record_exist(type_id):
                self.session.add(LastUpdateTimestampTable(type_id=type_id))
                self.write_to_db()
                print 'new record created in Timestamp table, id = ', type_id

    def check_if_record_exist(self,type_id):
        if isinstance(type_id,str):
            query = self.session.query(LastUpdateTimestampTable)

            if query.get(type_id):
                return True
            else:
                return False


def test01():
    import datetime
    db_interface = LastUpdateTimestampInterface()
    #db_interface.get_log_file_last_update_timestamp('Aptio')

    file_timestamp = datetime.datetime.strptime("2016-06-07 12:13:56", "%Y-%m-%d %H:%M:%S")
    record_timestamp = datetime.datetime.strptime("2016-06-07 13:14:45", "%Y-%m-%d %H:%M:%S")


    db_interface.set_log_file_last_update_timestamp(type_id='Aptio',timestamp=file_timestamp)
    db_interface.set_record_last_update_timestamp(type_id='Aptio',timestamp=record_timestamp)

    dt1 = db_interface.get_log_file_last_update_timestamp('Aptio')
    dt2 = db_interface.get_record_last_update_timestamp('Aptio')

    '''
    print 'dt1:'
    print type(dt1), ' : ', dt1

    print 'dt2:'
    print type(dt2), ' : ', dt2

    print dt1 > dt2
    '''

def reset_all_timestamp():
    import datetime
    db_interface = LastUpdateTimestampInterface()

    file_timestamp = datetime.datetime.strptime("2000-06-07 12:13:56", "%Y-%m-%d %H:%M:%S")
    record_timestamp = datetime.datetime.strptime("2000-06-07 13:14:45", "%Y-%m-%d %H:%M:%S")


    db_interface.set_log_file_last_update_timestamp(type_id='Flaxlab',timestamp=file_timestamp)
    db_interface.set_record_last_update_timestamp(type_id='Flaxlab',timestamp=record_timestamp)

    dt1 = db_interface.get_log_file_last_update_timestamp('Flaxlab')
    dt2 = db_interface.get_record_last_update_timestamp('Flaxlab')

    print 'Flaxlab log file update timestamp', dt1
    print 'Flaxlab record update timestamp', dt2

    ############################################################################################

    file_timestamp = datetime.datetime.strptime("2000-06-07 12:13:56", "%Y-%m-%d %H:%M:%S")
    record_timestamp = datetime.datetime.strptime("2000-06-07 13:14:45", "%Y-%m-%d %H:%M:%S")

    db_interface.set_log_file_last_update_timestamp(type_id='LIS_Out_Result', timestamp=file_timestamp)
    db_interface.set_record_last_update_timestamp(type_id='LIS_Out_Result', timestamp=record_timestamp)

    dt1 = db_interface.get_log_file_last_update_timestamp('LIS_Out_Result')
    dt2 = db_interface.get_record_last_update_timestamp('LIS_Out_Result')

    print 'LIS_Out_Result log file update timestamp', dt1
    print 'LIS_Out_Result record update timestamp', dt2


if __name__ == '__main__':
    reset_all_timestamp()