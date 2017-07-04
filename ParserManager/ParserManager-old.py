from threading import Thread
import os
import time
from threading import Timer

from CentralinkLogParser.Advia2400Parser import Advia2400Parser
from CentralinkLogParser.CentaurParser import CentaurParser
from CentralinkLogParser.LasReceiveParser import LasReceiveParser
from CentralinkLogParser.LisInParser import LisInParser
from CentralinkLogParser.LisOutParser import LisOutParser
from AptioLogParser.FlexlabLogParser import FlexlabControlParser

from DBInterface.TAT_Interface import TAT_Interface,TAT_Update_Timestamp_Interface

from FilesFilter.FilesFilter import FilesFilter

FILE_SCAN_INTERVAL = 1*60  #1 minutes of scan interval.
TRANSLATOR_LOG_FOLDER = r'F:\Zhongshan\log_centralink_20161110\trl'
CONTROL_LOG_FOLDER = r'F:\Zhongshan\log_aptio_20161110\Log'

class ParserManager():
    """
    manager of all parsers.
    """
    def __init__(self):
        self.advia_parser = Advia2400Parser()
        self.centaur_parser = CentaurParser()
        self.las_receive_parser = LasReceiveParser()
        self.lis_in_parser = LisInParser()
        self.lis_out_parser = LisOutParser()
        self.flexlab_parser = FlexlabControlParser()

        self.timing_exec_func()
        #self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        #self.timer.start()

    def timing_exec_func(self):
        print 'excuting...'
        ISOTIMEFORMAT='%Y-%m-%d %X'
        print  time.strftime(ISOTIMEFORMAT,time.localtime())
        self.parser()
        db_interface = TAT_Interface()
        db_interface.update_all_fields()
        self.timer = Timer(FILE_SCAN_INTERVAL,self.timing_exec_func)
        self.timer.start()
        print  time.strftime(ISOTIMEFORMAT,time.localtime())
        print 'end of execut'

    def parser_in_multithreads(self,trl_log_folder_path,start_date,end_date):
        advia_log_list = []
        centaur_log_list = []
        las_receive_log_list = []
        lis_in_log_list = []
        lis_out_log_list = []

        dir_list = os.listdir(trl_log_folder_path)
        for dir in dir_list:
            if isinstance(dir,str):
                if dir.startswith(r'Advia2400') or dir.startswith(r'Advia1800'):
                    #advia_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    advia_log_list += self.advia_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'advia log list: ', advia_log_list
                elif dir.startswith(r'CentaurXP'):
                    #centaur_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    centaur_log_list += self.centaur_parser.pre_work(os.path.join(trl_log_folder_path, dir))
                    print 'centaur log list: ', centaur_log_list
                elif r'Auto_Receive' == dir:
                    #las_receive_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    las_receive_log_list = self.las_receive_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'las log list: ', las_receive_log_list
                elif r'LIS_IN_Translator' == dir:
                    #lis_in_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    lis_in_log_list = self.lis_in_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'lis in log list: ', lis_in_log_list
                elif r'LIS_OUT_Translator' == dir:
                    #lis_out_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    lis_out_log_list = self.lis_out_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'lis out log list: ', lis_out_log_list

        parser_threads = []

        parser_threads.append(Thread(target=self.advia_parser.work,args=(advia_log_list,)))
        parser_threads.append(Thread(target=self.centaur_parser.work, args=(centaur_log_list,)))
        parser_threads.append(Thread(target=self.las_receive_parser.work,args=(las_receive_log_list,)))
        parser_threads.append(Thread(target=self.lis_in_parser.work,args=(lis_in_log_list,)))
        parser_threads.append(Thread(target=self.lis_out_parser.work,args=(lis_out_log_list,)))

        for t in parser_threads:
            #t.setDaemon(True)
            t.start()

    def centralink_log_parser(self,trl_log_folder_path,start_date=None,end_date=None):
        advia_log_list = []
        centaur_log_list = []
        las_receive_log_list = []
        lis_in_log_list = []
        lis_out_log_list = []

        dir_list = os.listdir(trl_log_folder_path)
        for dir in dir_list:
            if isinstance(dir,str):
                if dir.startswith(r'Advia2400') or dir.startswith(r'Advia1800'):
                    #advia_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    advia_log_list += self.advia_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'advia log list: ', advia_log_list
                elif dir.startswith(r'CentaurXP'):
                    #centaur_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    centaur_log_list += self.centaur_parser.pre_work(os.path.join(trl_log_folder_path, dir))
                    print 'centaur log list: ', centaur_log_list
                elif r'Auto_Receive' == dir:
                    #las_receive_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    las_receive_log_list = self.las_receive_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'las log list: ', las_receive_log_list
                elif r'LIS_IN_Translator' == dir:
                    #lis_in_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    lis_in_log_list = self.lis_in_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'lis in log list: ', lis_in_log_list
                elif r'LIS_OUT_Translator' == dir:
                    #lis_out_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                    lis_out_log_list = self.lis_out_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                    print 'lis out log list: ', lis_out_log_list

        self.advia_parser.work(advia_log_list)
        self.centaur_parser.work(centaur_log_list)
        self.las_receive_parser.work(las_receive_log_list)
        self.lis_in_parser.work(lis_in_log_list)
        self.lis_out_parser.work(lis_out_log_list)

    def flexlab_log_parser(self,control_log_folder_path,start_date=None,end_date=None):
        flexlab_log_file_list = []

        flexlab_log_file_list = self.flexlab_parser.pre_work(control_log_folder_path)
        print flexlab_log_file_list
        print len(flexlab_log_file_list)
        self.flexlab_parser.work(flexlab_log_file_list)

    def parser(self):
        print 'start of centralink log file parsing...'
        self.centralink_log_parser(TRANSLATOR_LOG_FOLDER)
        print 'end of centralink log file parsing...'
        print 'start of flexlab log file parsing...'
        self.flexlab_log_parser(CONTROL_LOG_FOLDER)
        print 'end of flexlab log file parsing...'

def test():
    parser_manager = ParserManager()
    trl_log_dir = r'D:\01_Automation\23_Experiential_Conclusions_2016\23_Zhongshan\trl_20160920_20161011'
    parser_manager.parser(trl_log_dir,None,None)


def test2():
    #trl_log_folder_path = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl'
    trl_log_folder_path=r'D:\01_Automation\23_Experiential_Conclusions_2016\23_Zhongshan\trl_20160920_20161011'
    start_date = None
    end_date = None

    advia_log_list = []
    centaur_log_list = []
    las_receive_log_list = []
    lis_in_log_list = []
    lis_out_log_list = []

    advia_parser = Advia2400Parser()
    centaur_parser = CentaurParser()
    las_receive_parser = LasReceiveParser()
    lis_in_parser = LisInParser()
    lis_out_parser = LisOutParser()

    dir_list = os.listdir(trl_log_folder_path)
    for dir in dir_list:
        if isinstance(dir,str):
            if dir.startswith(r'Advia2400') or dir.startswith(r'Advia1800'):
                #advia_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                advia_log_list += advia_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                print 'advia log list: ', advia_log_list
            elif dir.startswith(r'CentaurXP'):
                #centaur_log_list += FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                centaur_log_list += centaur_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                print 'centaur log list: ', centaur_log_list
            elif r'Auto_Receive' == dir:
                #las_receive_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                las_receive_log_list = las_receive_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                print 'las log list: ', las_receive_log_list
            elif r'LIS_IN_Translator' == dir:
                #lis_in_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                lis_in_log_list = lis_in_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                print 'lis in log list: ', lis_in_log_list
            elif r'LIS_OUT_Translator' == dir:
                #lis_out_log_list = FilesFilter.get_files_list(os.path.join(trl_log_folder_path,dir),start_date,end_date)
                lis_out_log_list = lis_out_parser.pre_work(os.path.join(trl_log_folder_path,dir))
                print 'lis out log list: ', lis_out_log_list

    advia_parser.work(advia_log_list)
    centaur_parser.work(centaur_log_list)
    las_receive_parser.work(las_receive_log_list)
    lis_in_parser.work(lis_in_log_list)
    lis_out_parser.work(lis_out_log_list)


def test3():
    interface = TAT_Update_Timestamp_Interface()
    #interface.check_if_record_exist(r'helll')
    #interface.check_if_record_exist(r'Advia2400')

    #interface.get_log_file_last_update_timestamp(r'Advia2400')
    #interface.get_record_last_update_timestamp(r'Advia2400')
    id = r'Advia2400'
    value = r'2016-11-09 12:12:29'

    interface.get_log_file_last_update_timestamp(id)
    interface.set_log_file_last_update_timestamp(id,value)
    interface.get_log_file_last_update_timestamp(id)

if __name__ == '__main__':
    '''
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    test2()
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    '''
    ParserManager()
    #test3()