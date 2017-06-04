import logging
import logging.handlers
import datetime
from pathlib import Path

root_path = Path('../data/log/')


class Logger:

    def __init__(self, new_type: str, select: int, log_level: int):

        self.current_time = datetime.datetime.now()
        current_datetime = self.current_time.strftime('%Y_%m_%d_%H_%M_%S')
        pathname = root_path
        fullname = pathname / current_datetime
        filename = str(fullname) + ".log"
        print(filename)
        if select == 1:
            self.object_manage(new_type, filename, log_level)
        elif select == 2:
            self.template_manage(new_type, filename, log_level)
        elif select == 3:
            self.signage_manage(new_type, filename, log_level)
        else:
            AttributeError()

    def object_manage(self, new_type: str, filename: str, log_level: int):
        self.manage(new_type, filename, log_level)

    def template_manage(self, new_type: str, filename: str, log_level: int):
        self.manage(new_type, filename, log_level)

    def signage_manage(self, new_type: str, filename: str, log_level: int):
        self.manage(new_type, filename, log_level)

    def manage(self, new_type: str, filename: str, log_level: int):
        level = ''
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
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
        time = self.current_time.strftime('%Y-%m-%d %H:%M:%S')
        f.write('{0} {1:10}: {2} loaded\n'.format(str(time), '[{}]'.format(level), new_type))
        f.close()
