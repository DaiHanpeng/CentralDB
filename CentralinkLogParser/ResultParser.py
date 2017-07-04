from datetime import datetime,date

from FilesFilter.FilesFilter import FilesFilter

from DBInterface.Tables import SampleTable,PatientTable,ResultTable
from DBInterface.PatientInterface import PatientInterface
from DBInterface.SampleInterface import SampleInterface
from DBInterface.ResultInterface import ResultInterface

from DBInterface.LastUpdateTimestampInterface import LastUpdateTimestampInterface


TABLE_UPDATE_TIMESTAMP_ID = r'LIS_Out_Result'

class ResultParser():
    """
    lis out log info parser.
    """
    def __init__(self):
        self.last_file_modified_timestamp = None   #last checked file modified time
        self.last_updated_record_timestamp = None #timestamp of the last updated record.

        timestamp_table_interface = LastUpdateTimestampInterface()
        self.last_file_modified_timestamp = timestamp_table_interface.get_log_file_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)
        self.last_updated_record_timestamp = timestamp_table_interface.get_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID)

        self.sample_result_map = {}# map sample id with it's resulting timestamp.87654wertyuiop[]

        self.result_list = list()

    def parse(self,log_file_list):
        self.patient_list = []
        self.sample_list = []
        self.result_list = []

        current_timestamp_newer_than_last = False

        patient = None
        sample = None
        result = None

        current_date_time = self.last_updated_record_timestamp

        if not log_file_list:
            print 'null log file list of Lis Out'
            return

        for item in log_file_list:
            print item
            file_content_list = []
            if isinstance(item,str):
                try:
                    lis_out_file_handler = open(item,mode='rU')
                    file_content_list = lis_out_file_handler.readlines()
                    #file_content_list.reverse()
                except Exception as e:
                    print 'file read failed!'
                    print 'exception:',e
                finally:
                    lis_out_file_handler.close()

            if file_content_list:
                for line in file_content_list:
                    if isinstance(line,str):
                        if line.startswith(r'L|1|'):
                            patient = None
                            sample = None
                            result = None
                        elif line.startswith(r'P|1|') and -1 <> line.find(r'Human^Human') and (True == current_timestamp_newer_than_last):
                            patient_info_list = line.split(r'|')
                            if len(patient_info_list) > 8:
                                pid = patient_info_list[2]
                                if not pid:
                                    continue
                                lname = patient_info_list[5]
                                birthday = patient_info_list[7]
                                if birthday:
                                    #print birthday
                                    birthday = datetime.strptime(birthday,'%Y%m%d').date()
                                else:
                                    birthday = None
                                sex = patient_info_list[8]
                                patient = PatientTable(pid=pid,\
                                                       lname=lname,\
                                                       birthday=birthday,\
                                                       sex=sex)
                                self.patient_list.append(patient)
                        elif line.startswith(r'O|1|') and -1 == line.find(r'||||Q|||') and patient:
                            sample_info_list = line.split(r'|')
                            if len(sample_info_list) > 15:
                                sid = sample_info_list[2]
                                if not sid:
                                    print 'no sample id!'
                                    continue
                                tube_type = sample_info_list[9].split(r'^')[-1]
                                sample_type = sample_info_list[15]
                                pid = patient.pid
                                sample = SampleTable(sid=sid,\
                                                     tube_type=tube_type,\
                                                     sample_type=sample_type,\
                                                     pid=pid)
                                self.sample_list.append(sample)
                        elif line.startswith(r'R|') and len(line.split(r'||')) > 1 and -1 <> line.find(r'^^^') and sample:
                            result_info_list = line.split(r'|')
                            if len(result_info_list) > 11:
                                test_name = result_info_list[2].split(r'^')[3]
                                dilution_profile = result_info_list[2].split(r'^')[4]
                                dilution_factor = result_info_list[2].split(r'^')[5]
                                aspect = result_info_list[2].split(r'^')[-2]
                                result = result_info_list[3]
                                dt = result_info_list[11]
                                if dt:
                                    dt = datetime.strptime(dt,'%Y%m%d%H%M%S')
                                else:
                                    dt = None
                                    print 'datetime is null: '+'sample_id: '+sample.sid
                                instrument_id = result_info_list[-1]
                                sid = sample.sid
                                result = ResultTable(test_name=test_name,\
                                                 dilution_profile=dilution_profile,\
                                                 dilution_factor=dilution_factor,\
                                                 result=result,\
                                                 datetime=dt,\
                                                 instrument_id=instrument_id,\
                                                 sid=sid,\
                                                 aspect=aspect)
                                self.result_list.append(result)
                        elif -1 <> line.find(r'INFO [IO-TCP]'):
                            dt = line.split(r'INFO [IO-TCP]')[1].strip()
                            dt = dt.split(r'.')[0]
                            dt = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
                            if (not current_date_time) or current_date_time < dt:
                                current_date_time = dt
                                if not current_timestamp_newer_than_last:
                                    current_timestamp_newer_than_last = True

        if (not self.last_updated_record_timestamp) or (current_date_time > self.last_updated_record_timestamp):
            self.last_updated_record_timestamp = current_date_time
            #update to db
            timestamp_table_interface = LastUpdateTimestampInterface()
            timestamp_table_interface.set_record_last_update_timestamp(TABLE_UPDATE_TIMESTAMP_ID,self.last_updated_record_timestamp)


    def to_db(self):
        db_patient_interface = PatientInterface()
        db_sample_interface = SampleInterface()
        db_result_interface = ResultInterface()

        print 'len of patient :' + str(len(self.patient_list))
        print 'len of sample  :' + str(len(self.sample_list))
        print 'len of result  :' + str(len(self.result_list))

        db_patient_interface.add_new_records(self.patient_list)
        db_sample_interface.add_new_records(self.sample_list)
        db_result_interface.add_new_records(self.result_list)


    def pre_work(self,log_folder):
        current_file_modified_timestamp = FilesFilter.get_latest_modified_timestamp(log_folder)
        current_file_modified_timestamp = datetime.fromtimestamp(current_file_modified_timestamp)
        log_file_list = FilesFilter.get_files_after_a_modified_timestamp(log_folder,self.last_file_modified_timestamp)
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
        return 'patient list:\n' +\
            '\n'.join(str(patient) for patient in self.patient_list)+'\n'+\
            'sample list:\n'+\
            '\n'.join(str(sample) for sample in self.sample_list)+'\n'\
            'result list:\n'+\
            '\n'.join(str(result) for result in self.result_list)


def test():
    result_parser = ResultParser()
    lis_out_log_folder = r'M:\trl\LIS_OUT_Translator'
    lis_out_log_file_list = result_parser.pre_work(lis_out_log_folder)
    result_parser.work(lis_out_log_file_list)
    #print result_parser

if __name__ == '__main__':
    test()