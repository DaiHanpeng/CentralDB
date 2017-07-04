import os
from datetime import *

class FilesFilter():
    """
    filter to get file list in a folder, which file modification time between[start_date,end_date]
    """
    @staticmethod
    def get_files_list(path_to_folder,start_date=None,end_date=None):
        file_list = []
        if start_date and end_date:
            if isinstance(start_date,date) and isinstance(end_date,date):
                folder_file_list = os.listdir(path_to_folder)
                for f in folder_file_list:
                    #print os.path.getmtime(f)
                    file_mtime = date.fromtimestamp(os.path.getmtime(f))
                    if start_date <= file_mtime <= end_date:
                        file_list.append(os.path.join(path_to_folder,f))
            else:
                print 'start or end datetime format error!'
        else:
            folder_file_list = os.listdir(path_to_folder)
            for f in folder_file_list:
                file_list.append(os.path.join(path_to_folder,f))
        return file_list


    @staticmethod
    def get_files_after_a_modified_timestamp(path_to_folder,modified_timestamp=None,startswith=r''):
        if (not isinstance(modified_timestamp,datetime)) or (not modified_timestamp):
            print 'parameter modified_timestamp error!'
            print modified_timestamp

        file_list = []
        folder_file_list = os.listdir(path_to_folder)
        filted_file_list = []

        for item in folder_file_list:
            if item.startswith(startswith):
                filted_file_list.append(os.path.join(path_to_folder,item))

        for f in filted_file_list:
            if (not modified_timestamp) or (modified_timestamp < datetime.fromtimestamp(os.path.getmtime(f))):
                file_list.append(f)

        return file_list

    @staticmethod
    def get_latest_modified_timestamp(path_to_folder,startswith=r''):
        latest_modified_timestamp = 0

        folder_file_list = os.listdir(path_to_folder)
        filted_file_list = []

        for item in folder_file_list:
            if item.startswith(startswith):
                filted_file_list.append(os.path.join(path_to_folder,item))

        for f in filted_file_list:
            if os.path.getmtime(f) > latest_modified_timestamp:
                latest_modified_timestamp = os.path.getmtime(f)
                #print latest_modified_timestamp

        return latest_modified_timestamp


def test():

    #files_filter = FilesFilter()

    start = '2016-05-19'
    end = '2016-05-21'
    start_date = datetime.strptime(start,'%Y-%m-%d').date()
    end_date = datetime.strptime(end,'%Y-%m-%d').date()

    #print end_date < start_date

    print FilesFilter.get_files_list('.',start_date,end_date)

    lis_in_log_folder = r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl\LIS_Translator_in'
    lis_in_log_file_list = FilesFilter.get_files_list(lis_in_log_folder)

    print lis_in_log_file_list


    '''
    # datetime and string conversion...
    start = '2016-05-20'
    end = '2016-05-21'

    start_date = datetime.strptime(start,'%Y-%m-%d').date()
    end_date = datetime.strptime(end,'%Y-%m-%d').date()

    print start_date,end_date
    '''

def test2():
    directory = r"F:\Zhongshan\log_aptio_20161110\Log"
    modified_timestamp = 1479292284.55

    files_arrays = FilesFilter.get_files_after_a_modified_timestamp(directory,modified_timestamp,'CONTROL')
    print files_arrays

def test3():
    directory = r"F:\Zhongshan\log_aptio_20161110\Log"
    print 'latest file timestamp:', FilesFilter.get_latest_modified_timestamp(directory,'CONTROL')
    print 'mtime for control.txt', os.path.getmtime(r'F:\Zhongshan\log_aptio_20161110\Log\control.txt')


if __name__ == '__main__':
    test2()
    test3()
    #print os.listdir(r'D:\01_Automation\23_Experiential_Conclusions_2016\19_Anhui_Provicial_Hospital\Log\trl')

