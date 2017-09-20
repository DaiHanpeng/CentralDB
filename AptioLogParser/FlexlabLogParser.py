from datetime import *
import zipfile
from zipfile import ZipFile
import os

from FilesFilter.FilesFilter import FilesFilter
from DBInterface.Tables import LasLogTable
from DBInterface.LasLogInterface import LasLogInterface

from DBInterface.LastUpdateTimestampInterface import LastUpdateTimestampInterface

TABLE_UPDATE_TIMESTAMP_ID = r'Flaxlab'

class LasLogParser():
    """
    Las log info parser
    """
    def __init__(self):
        self.last_file_modified_timestamp = None   #last checked file modified time
        self.last_updated_record_timestamp = None #timestamp of the last updated record.

        timestamp_table_interface = LastUpdateTimestampInterface()
        self.last_file_modified_timestamp = timestamp_table_interface.get_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)
        self.last_updated_record_timestamp = timestamp_table_interface.get_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)

        self.las_log_list = list()

    def parse(self,log_file_list):
        self.las_log_list = []

        current_date_time = None
        last_updated_record_timestamp = self.last_updated_record_timestamp

        if not log_file_list:
            print 'null log file list of Aptio Control'
            return

        #print log_file_list
        for item in log_file_list:
            print item, "is being processing..."
            file_content_list = []
            if isinstance(item,str) and os.path.isfile(item):
                if not zipfile.is_zipfile(item):
                    try:
                        flexlab_file_handler = open(item)
                        file_content_list = flexlab_file_handler.readlines()
                        file_content_list.reverse()
                    except Exception as e:
                        print 'file read failed!'
                        print 'exception:',e
                    finally:
                        flexlab_file_handler.close()
                else:
                    with ZipFile(item, 'r') as open_zip_file:
                        #print open_zip_file.namelist()
                        file_list = open_zip_file.namelist()
                        for log_file in file_list:
                            if isinstance(log_file,str):
                                if log_file.startswith(r'CONTROL'):
                                    with open_zip_file.open(log_file) as opened_control_log_file:
                                        file_content_list += opened_control_log_file.readlines()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        #parsing information for TAT statistic.
                        if -1 <> line.find(r' ADD ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            current_date_time = datetime.strptime(current_date_time,'%Y%m%d%H%M%S')
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' ADD ')[1].split(r'|')[1]
                                carrier_id = line.split(r' ADD ')[1].split(r'|')[0].strip()
                                node_type = line.split(r' ADD ')[0].split()[-1].strip()
                                node_id = line.split(r' ADD ')[0].split()[-2].split('"')[-1].strip()
                                if sample_id:
                                    self.las_log_list.append(LasLogTable(sample_id=sample_id,\
                                                             carrier_id=carrier_id,\
                                                             timestamp=current_date_time,\
                                                             log_code='ADD',\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )
                        elif -1 <> line.find(r' RETURNED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            current_date_time = datetime.strptime(current_date_time, '%Y%m%d%H%M%S')
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' RETURNED ')[1].split(r'^')[1]
                                carrier_id = line.split(r' RETURNED ')[1].split(r'^')[0].strip()
                                node_type = line.split(r' RETURNED ')[0].split()[-1].strip()
                                node_id = line.split(r' RETURNED ')[0].split()[-2].split('"')[-1].strip()
                                error_code = sample_id = line.split(r' RETURNED ')[1].split(r'^')[2].strip()
                                if sample_id:
                                    self.las_log_list.append(LasLogTable(sample_id=sample_id,\
                                                             carrier_id=carrier_id,\
                                                             timestamp=current_date_time,\
                                                             log_code='RETURN',\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )
                                if error_code and (error_code <> r'0000'):
                                    # common error codes in <error handling.ini>
                                    if error_code.startswith((r'80',r'81',r'82',r'SC',r'S0')):
                                        node_type = 'ALL'
                                    self.las_log_list.append(LasLogTable(sample_id=sample_id,\
                                                             carrier_id=carrier_id,\
                                                             timestamp=current_date_time,\
                                                             log_code=error_code,\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )
                        elif -1 <> line.find(r' DIVERTED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            current_date_time = datetime.strptime(current_date_time, '%Y%m%d%H%M%S')
                            if current_date_time >= self.last_updated_record_timestamp:
                                #sample_id = line.split(r' DIVERTED ')[1].split(r'^')[1]
                                carrier_id = line.split(r' DIVERTED ')[1].split(r'^')[0].strip()
                                node_type = line.split(r' DIVERTED ')[0].split()[-1].strip()
                                node_id = line.split(r' DIVERTED ')[0].split()[-2].split('"')[-1].strip()
                                if carrier_id:
                                    self.las_log_list.append(LasLogTable(sample_id=None,\
                                                             carrier_id=carrier_id,\
                                                             timestamp=current_date_time,\
                                                             log_code='DIVERT',\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )
                        elif -1 <> line.find(r' SAMPLE-DETECTED ') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            current_date_time = datetime.strptime(current_date_time, '%Y%m%d%H%M%S')
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' SAMPLE-DETECTED ')[1].split(r'^')[1]
                                #carrier_id = line.split(r' RETURNED ')[1].split(r'^')[0].strip()
                                node_type = line.split(r' SAMPLE-DETECTED ')[0].split()[-1].strip()
                                node_id = line.split(r' SAMPLE-DETECTED ')[0].split()[-2].split('"')[-1].strip()
                                if sample_id:
                                    self.las_log_list.append(LasLogTable(sample_id=sample_id,\
                                                             carrier_id=None,\
                                                             timestamp=current_date_time,\
                                                             log_code='DECTECTED',\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )
                        #<SRM SAMPLE-LOCATION ^> as storage time stamp
                        elif -1 <> line.find(r' SAMPLE-LOCATION ^') and -1 <> line.find(r'timestamp='):
                            current_date_time = line.split(r'timestamp="')[1].split(r'"')[0]
                            current_date_time = datetime.strptime(current_date_time, '%Y%m%d%H%M%S')
                            if current_date_time >= self.last_updated_record_timestamp:
                                sample_id = line.split(r' SAMPLE-LOCATION ^')[1].split(r'^')[0]
                                #carrier_id = line.split(r' RETURNED ')[1].split(r'^')[0].strip()
                                node_type = line.split(r' SAMPLE-LOCATION ^')[0].split()[-1].strip()
                                node_id = line.split(r' SAMPLE-LOCATION ^')[0].split()[-2].split('"')[-1].strip()
                                if sample_id:
                                    self.las_log_list.append(LasLogTable(sample_id=sample_id,\
                                                             carrier_id=None,\
                                                             timestamp=current_date_time,\
                                                             log_code='LOCATION',\
                                                             node_type=node_type,\
                                                             node_id=node_id)
                                                             )

                        #update timestamp.
                        # print 'last_updated_record_timestamp'
                        # print last_updated_record_timestamp
                        # print 'current_date_time'
                        # print current_date_time
                        if (not last_updated_record_timestamp) or\
                                ((current_date_time is not None) and (last_updated_record_timestamp < current_date_time)):
                            last_updated_record_timestamp = current_date_time

        if last_updated_record_timestamp > self.last_updated_record_timestamp:
            self.last_updated_record_timestamp = last_updated_record_timestamp
            #update to db
            timestamp_table_interface = LastUpdateTimestampInterface()
            timestamp_table_interface.set_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_updated_record_timestamp)

    def to_db(self):
        db_interface = LasLogInterface()
        db_interface.update_records(self.las_log_list)

    def pre_work(self,log_folder):
        #please keep this evaluate sequence...
        current_file_modified_timestamp = FilesFilter.get_latest_modified_timestamp(log_folder,r'CONTROL')
        log_file_list = FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp,r'CONTROL')
        log_file_list += FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp,r'Logs-')
        if (not self.last_file_modified_timestamp) or (current_file_modified_timestamp > self.last_file_modified_timestamp):
            self.last_file_modified_timestamp = current_file_modified_timestamp
            #update to db
            timestamp_table_interface = LastUpdateTimestampInterface()
            timestamp_table_interface.set_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_file_modified_timestamp)


        return log_file_list

    def work(self,log_file_list):
        self.parse(log_file_list)
        self.to_db()

    def __repr__(self):
        return 'las log list:\n' +\
            '\n'.join(str(las_log) for las_log in self.las_log_list)

def test1():
    flexlab_parser = LasLogParser()

    flexlab_log_folder = r'D:\01_Automation\24_Experiential_Conclusion_2017\30_TaiWan_UCL_Support\OrderNotSent2Automation\FlexLab36 - 20170912\Log'

    flexlab_log_file_list = flexlab_parser.pre_work(flexlab_log_folder)
    print flexlab_log_file_list
    print len(flexlab_log_file_list)
    flexlab_parser.work(flexlab_log_file_list)
    #print flexlab_parser.las_log_list

if __name__ == '__main__':
    test1()