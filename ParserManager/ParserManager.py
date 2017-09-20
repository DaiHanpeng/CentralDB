from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor

from CentralinkLogParser.ResultParser import ResultParser
from AptioLogParser.ReagentInventoryParser import ReagentInventoryParser

from AptioLogParser.FlexlabLogParser import LasLogParser


FILE_SCAN_INTERVAL = 1*60  #1 minutes of scan interval.

CENTRALINK_RESULT_SCAN_INTERVAL = 5*60  #5 minutes of scan interval.
REAGENT_INVENTORY_SCAN_INTERVAL = 1*60  #1 minutes of scan interval.
LAS_LOG_SCAN_INTERVAL = 5*60  #5 minutes of scan interval.


#LIS_OUT_LOG_FOLDER = r'M:\trl\LIS_OUT_Translator'
#CONTROL_LOG_FOLDER = r'N:\Log'
LIS_OUT_LOG_FOLDER = r'D:\01_Automation\23_Experiential_Conclusions_2016\23_Zhongshan\trl_20160920_20161011\LIS_OUT_Translator'
CONTROL_LOG_FOLDER = r'D:\01_Automation\24_Experiential_Conclusion_2017\30_TaiWan_UCL_Support\OrderNotSent2Automation\FlexLab36 - 20170912\Log'

class ParserManager():
    """
    manager of all parsers.
    """

    scheduler = None

    @staticmethod
    def jod_result_parse():
        print 'jod: result parse started'
        result_parser = ResultParser()
        lis_out_file_list = result_parser.pre_work(LIS_OUT_LOG_FOLDER)
        result_parser.work(lis_out_file_list)
        print 'jod: result parse ended'

    @staticmethod
    def jod_reagent_inventory_parse():
        print 'jod: reagent inventory parse started'
        reagent_inventory_parser = ReagentInventoryParser()
        control_lig_file = reagent_inventory_parser.pre_work(CONTROL_LOG_FOLDER)
        reagent_inventory_parser.work(control_lig_file)
        print 'jod: reagent inventory parse ended'

    @staticmethod
    def jod_las_log_parse():
        print 'jod: las log parse started'
        las_log_parser = LasLogParser()
        control_lig_file = las_log_parser.pre_work(CONTROL_LOG_FOLDER)
        las_log_parser.work(control_lig_file)
        print 'jod: las log parse ended'

    @staticmethod
    def job_testing():
        print 'hello, this is a daemon jod schedule to run every minute !'

    @classmethod
    def jod_initialize(cls):
        executors = {
                        'default': ThreadPoolExecutor(5),\
                        'processpool': ProcessPoolExecutor(2)\
                     }
        cls.scheduler = BackgroundScheduler(executors=executors)
        cls.scheduler.add_job(cls.jod_result_parse, 'interval', seconds=CENTRALINK_RESULT_SCAN_INTERVAL)
        cls.scheduler.add_job(cls.jod_reagent_inventory_parse, 'interval', seconds=REAGENT_INVENTORY_SCAN_INTERVAL)
        cls.scheduler.add_job(cls.jod_las_log_parse, 'interval', seconds=LAS_LOG_SCAN_INTERVAL)
        cls.scheduler.add_job(cls.job_testing, 'interval', seconds=FILE_SCAN_INTERVAL)
        print 'job added.'

    @classmethod
    def start_jods(cls):
        if cls.scheduler:
            cls.scheduler.start()
            print 'jods started'

    @classmethod
    def first_run(cls):
        print 'run first time started...'
        cls.jod_result_parse()
        cls.jod_reagent_inventory_parse()
        cls.jod_las_log_parse()
        print 'run first time finished...'


if __name__ == '__main__':
    '''
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    test2()
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    '''
    #parser_manager = ParserManager()
    # run first time may take a long time!
    ParserManager.first_run()
    # pass jobs to scheduler and kick start
    ParserManager.jod_initialize()
    ParserManager.start_jods()
    ParserManager.job_testing()
    while True:
        pass
    #test3()