import logging
import logging.handlers
import datetime
from pathlib import Path

root_path = Path('../data/log/')


class Logger:
    current_time = datetime.datetime.now()
    current_datetime = current_time.strftime('%Y_%m_%d_%H_%M_%S')
    pathname = root_path
    fullname = pathname / current_datetime
    filename = str(fullname) + ".log"
    f = open(filename, 'w')
    f.close()

    def info(self, msg: str):
        log_type = 'info'
        self.write_log(msg, log_type)

    def warn(self, msg: str):
        log_type = 'warn'
        self.write_log(msg, log_type)

    def error(self, msg: str):
        log_type = 'error'
        self.write_log(msg, log_type)

    def write_log(self, msg: str, log_type: str):
        f = open(Logger.filename, 'a')
        current_time = datetime.datetime.now()
        time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        f.write('{0} {1:10}: {2} \n'.format(str(time), '[{}]'.format(log_type), msg))
        f.close()
