from datetime import datetime
import os

from FilesFilter.FilesFilter import FilesFilter
from DBInterface.Tables import LastUpdateTimestampTable
from DBInterface.Tables import ReagentInventoryTable
from DBInterface.ReagentInventoryInterface import ReagentInventoryInterface
from DBInterface.LastUpdateTimestampInterface import LastUpdateTimestampTable,LastUpdateTimestampInterface
from DBInterface.SampleLocationInterface import SampleLocationTable,SampleLocationInterface

from ReagentInfoDef import ReagentInfoItem,InstrumentReagentInfo,SystemReagentInfo

TABLE_UPDATE_TIMESTAMP_ID = r'Flaxlab'

class ReagentInventoryParser():
    """
    Flexlab Control log info parser for reagent inventory
    """
    def __init__(self):
        self.last_file_modified_timestamp = None   #last checked file modified time
        self.last_updated_record_timestamp = None #timestamp of the last updated record.

        timestamp_table_interface = LastUpdateTimestampInterface()
        self.last_file_modified_timestamp = timestamp_table_interface.get_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)
        self.last_updated_record_timestamp = timestamp_table_interface.get_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)

        self.system_reagent = SystemReagentInfo()
        # self.sample_location_list = []

    def parse(self,log_file):
        current_date_time = None
        last_updated_record_timestamp = self.last_updated_record_timestamp

        # self.sample_location_list = []

        file_content_list = []
        if isinstance(log_file,str) and os.path.isfile(log_file):
            try:
                flexlab_file_handler = open(log_file)
                file_content_list = flexlab_file_handler.readlines()
                file_content_list.reverse()
            except Exception as e:
                print 'file read failed!'
                print 'exception:',e
            finally:
                flexlab_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if line.find('INVENTORY') > 0:
                            inventory_info = line.split(' ')
                            time_stamp = inventory_info[1].split(r'"')[1]
                            #convert time_stamp from str to datetime format.
                            time_stamp = datetime.strptime(time_stamp,'%Y%m%d%H%M%S')
                            instrument_id = inventory_info[4].split(r'"')[1]
                            instrument_type = inventory_info[5]

                            # if instrument reagent info is found, update its time stamp, otherwise, create a new one.
                            # time stamp is older than current time stamp is ignored.
                            if (not last_updated_record_timestamp) or (time_stamp > last_updated_record_timestamp):
                                reagent_inventory_info = inventory_info[7]
                                reagent_item_list = []
                                if isinstance(reagent_inventory_info, str):
                                    inventory_info_list = reagent_inventory_info.split("\\")
                                    for item in inventory_info_list:
                                        if item.find("^") > 0:
                                            reagent_pair = item.split("^")
                                            reagent_item_list.append(ReagentInfoItem(reagent_name=reagent_pair[-3],\
                                                                                     reagent_count=reagent_pair[-2]))
                                instr_reagent_info = InstrumentReagentInfo(instr_id=instrument_id,\
                                                                           instr_type=instrument_type,\
                                                                           time_stamp=time_stamp,\
                                                                           reagent_info_list=reagent_item_list)
                                self.system_reagent.update_instrument_reagent_inventory(instr_reagent_info)

                            #update timestamp.
                            if (not current_date_time) or (current_date_time < time_stamp):
                                current_date_time = time_stamp

                            if last_updated_record_timestamp and (time_stamp <= last_updated_record_timestamp):
                                break

                        # elif line.find(r'SAMPLE-DETECTED')>0:
                        #     info_list = line.split()
                        #     if len(info_list) > 7:
                        #         sid = None
                        #         timestamp = None
                        #         location = None
                        #         if len(info_list[-2].rsplit(r'^')) > 2:
                        #             sid = info_list[-2].rsplit(r'^')[1]
                        #         if info_list[1].find(r'timestamp')>0 and info_list[1].find(r'"') > 1:
                        #             timestamp = info_list[1].split(r'"')[1]
                        #         location = 'Track'
                        #         #insert the record into the list
                        #         if sid and timestamp and location:
                        #             sample_location = SampleLocationTable(sid=sid,location=location,timestamp=timestamp)
                        #             duplicated_found = False
                        #             for item in self.sample_location_list:
                        #                 if isinstance(item,SampleLocationTable):
                        #                     if item.sid == sid:
                        #                         duplicated_found = True
                        #                         break
                        #             if not duplicated_found:
                        #                 self.sample_location_list.append(sample_location)
                        # elif line.find(r'SAMPLE-LOCATION')>0:
                        #     info_list = line.split()
                        #     if len(info_list) > 7:
                        #         sid = None
                        #         timestamp = None
                        #         location = None
                        #         if len(info_list[-2].rsplit(r'^')) > 2:
                        #             sid = info_list[-2].rsplit(r'^')[1]
                        #         if info_list[1].find(r'timestamp')>0 and info_list[1].find(r'"') > 1:
                        #             timestamp = info_list[1].split(r'"')[1]
                        #         location = info_list[5]
                        #         #insert the record into the list
                        #         if sid and timestamp and location:
                        #             sample_location = SampleLocationTable(sid=sid,location=location,timestamp=timestamp)
                        #             duplicated_found = False
                        #             for item in self.sample_location_list:
                        #                 if isinstance(item,SampleLocationTable):
                        #                     if item.sid == sid:
                        #                         duplicated_found = True
                        #                         break
                        #             if not duplicated_found:
                        #                 self.sample_location_list.append(sample_location)


        if not self.last_updated_record_timestamp or (current_date_time > self.last_updated_record_timestamp):
            self.last_updated_record_timestamp = current_date_time
            #update to db
            timestamp_table_interface = LastUpdateTimestampInterface()
            timestamp_table_interface.set_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_updated_record_timestamp)

    def to_db(self):
        self.reagent_to_db()
        # print 'len of sample location list:'
        # print len(self.sample_location_list)
        # self.sample_location_to_db()

    # def sample_location_to_db(self):
    #     db_interface = SampleLocationInterface()
    #     if self.sample_location_list:
    #         db_interface.add_new_records(self.sample_location_list)

    def reagent_to_db(self):
        db_interface = ReagentInventoryInterface()

        for instr in self.system_reagent.system_reagent:
            if isinstance(instr,InstrumentReagentInfo):
                for item in instr.reagent_info_list:
                    if isinstance(item,ReagentInfoItem):
                        db_interface.update_record(node_id=instr.instrument_id,\
                                                   node_type=instr.instrument_type,\
                                                   reagent_name=item.reagent_name,\
                                                   reagent_type='All',\
                                                   reagent_count=item.reagent_count,\
                                                   updated_timestamp=instr.time_stamp)

    def pre_work(self,log_folder):
        return os.path.join(log_folder,'CONTROL.TXT')

    def work(self,log_file):
        self.parse(log_file)
        self.to_db()

    def __repr__(self):
        return 'parserd reagent info:' + str(self.system_reagent).join(str(item) for item in self.sample_location_list)

def mytest():
    reagent_inventory_parser = ReagentInventoryParser()

    #flexlab_log_folder = r'N:\Log'
    flexlab_log_folder = r'F:\HK\GHK\centralDB'


    flexlab_log_file = reagent_inventory_parser.pre_work(flexlab_log_folder)
    print flexlab_log_file
    reagent_inventory_parser.work(flexlab_log_file)
    print reagent_inventory_parser

if __name__ == '__main__':
    mytest()