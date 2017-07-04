from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor

from CentralinkLogParser.ResultParser import ResultParser
from AptioLogParser.ReagentInventoryParser import ReagentInventoryParser


FILE_SCAN_INTERVAL = 1*60  #1 minutes of scan interval.

LIS_OUT_LOG_FOLDER = r'M:\trl\LIS_OUT_Translator'
CONTROL_LOG_FOLDER = r'N:\Log'


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
    def job_testing():
        print 'hello, this is a tesing jod!'

    @classmethod
    def jod_initialize(cls):
        executors = {
                        'default': ThreadPoolExecutor(5),\
                        'processpool': ProcessPoolExecutor(2)\
                     }
        cls.scheduler = BackgroundScheduler(executors=executors)
        cls.scheduler.add_job(cls.jod_result_parse, 'interval', seconds=300)
        cls.scheduler.add_job(cls.jod_reagent_inventory_parse, 'interval', seconds=100)
        cls.scheduler.add_job(cls.job_testing, 'interval', seconds=60)
        print 'job added.'

    @classmethod
    def start_jods(cls):
        if cls.scheduler:
            cls.scheduler.start()
            print 'jods started'


if __name__ == '__main__':
    '''
    ISOTIMEFORMAT='%Y-%m-%d %X'
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    test2()
    print  time.strftime(ISOTIMEFORMAT,time.localtime())
    '''
    #parser_manager = ParserManager()
    ParserManager.jod_initialize()
    ParserManager.start_jods()
    ParserManager.job_testing()
    while True:
        pass
    #test3()