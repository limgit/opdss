import os
import logging
import logging.handlers
import datetime




class Logger:

    def __init__(self, new_type: str, select: int, log_level: int):


        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        current_time = datetime.datetime.now()
        currentDatetime = current_time.strftime('%Y_%m_%d_%H_%M_%S')

        #filename = 'C:/Users/sumin/PycharmProjects/guess/data/log/('current_time').log'
        pathname = 'C:/Users/sumin/PycharmProjects/guess/data/log/'
        fullname = pathname + currentDatetime

        filename = fullname + ".log"

        if select == 1:
            self.object_manage(new_type, filename, log_level)
        elif select == 2:
            self.template_manage(new_type, filename, log_level)
        elif select == 3:
            self.signamge_manage(new_type, filename, log_level)
        else:
            AttributeError()

    def object_manage(self, new_type: str, filename: str, log_level: int):
        """f = open(filename, 'a')
        f.write('{} loaded\n'.format(new_type))
        print('{} loaded'.format(new_type))
        f.close()"""
        self.manage(new_type, filename, log_level)

    def template_manage(self, new_type: str, filename: str, log_level: int):
        """f = open(filename, 'a')
        f.write('{} loaded\n'.format(new_type))
        print('{} loaded'.format(new_type))
        f.close()"""
        self.manage(new_type, filename, log_level)

    def signamge_manage(self, new_type: str, filename: str, log_level: int):
        """f = open(filename, 'a')
        f.write('{} loaded\n'.format(new_type))
        print('{} loaded'.format(new_type))
        f.close()"""
        self.manage(new_type, filename, log_level)

    def manage(self, new_type: str, filename: str, log_level: int):
        level = ''
        f = open(filename, 'a')
        if log_level == 1:
            level = 'info'
        elif log_level == 2:
            level = 'warning'
        elif log_level == 3:
            level = 'error'
        elif log_level == 4:
            level = 'critical'
        else:
            AttributeError()
        f.write('log_level :' + level + '   ==> ' + '{} loaded\n'.format(new_type))
        print('{} loaded'.format(new_type))
        f.close()