from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Tables import BaseModel,ReagentInventoryTable

class ReagentInventoryInterface():
    """
    db interface for reagent_inventory table.
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
                      node_id='NodeID', \
                      node_type='NodeType', \
                      reagent_name='ReagentName', \
                      reagent_type='All', \
                      reagent_count=None, \
                      reagent_warn_threshold=None, \
                      reagent_err_threshold=None, \
                      expire_date_time=None, \
                      reagent_pack_lot=None,\
                      updated_timestamp=None):
        #self.session.add(PatientTable(pid,fname,lname,birthday,sex,location))
        # use merge() instead od add() to avoid duplicated insert error from MySQL.
        self.session.merge(ReagentInventoryTable(node_id=node_id,\
                                                 node_type=node_type,\
                                                 reagent_name=reagent_name,\
                                                 reagent_type=reagent_type,\
                                                 reagent_count=reagent_count,\
                                                 reagent_warn_threshold=reagent_warn_threshold,\
                                                 reagent_err_threshold=reagent_err_threshold,\
                                                 expire_date_time=expire_date_time,\
                                                 reagent_pack_lot=reagent_pack_lot,\
                                                 updated_timestamp=updated_timestamp))
        self.write_to_db()

    def update_records(self, patient_list):
        if isinstance(patient_list,list):
            for item in patient_list:
                if isinstance(item,ReagentInventoryTable):
                    self.session.merge(ReagentInventoryTable(node_id=item.node_id,\
                                                             node_type=item.node_type,\
                                                             reagent_name=item.reagent_name,\
                                                             reagent_type=item.reagent_type,\
                                                             reagent_count=item.reagent_count,\
                                                             reagent_warn_threshold=item.reagent_warn_threshold,\
                                                             reagent_err_threshold=item.reagent_err_threshold,\
                                                             expire_date_time=item.expire_date_time,\
                                                             reagent_pack_lot=item.reagent_pack_lot,\
                                                             updated_timestamp=item.updated_timestamp))

            self.write_to_db()

    def write_to_db(self):
        try:
            self.session.flush()
            self.session.commit()
        except Exception as ex:
            print 'database write failed!'
            print ex

def test01():
    db_interface = ReagentInventoryInterface()
    db_interface.update_record(node_id='003', node_type='CEN', reagent_name='TSH', reagent_count=88)
    db_interface.update_record(node_id='003', node_type='CEN', reagent_name='ThCG', reagent_count=23)
    db_interface.update_record(node_id='004', node_type='A24', reagent_name='Ca', reagent_count=356)
    db_interface.update_record(node_id='004', node_type='A24', reagent_name='K', reagent_count=378)
    #db_interface.update_record(22334455)
    db_interface.write_to_db()

if __name__ == '__main__':
    test01()