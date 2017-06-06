import datetime
from pathlib import Path

root_path = Path('../../data/log/')
current_time = datetime.datetime.now()
current_datetime = current_time.strftime('%Y_%m_%d_%H_%M_%S')
pathname = root_path
fullname = pathname / current_datetime
filename = str(fullname) + ".log"


def write_log(msg: str, log_type: str):
    f = open(filename, 'a')
    log_current_time = datetime.datetime.now()
    time = log_current_time.strftime('%Y-%m-%d %H:%M:%S')
    f.write('{0} {1:10}: {2} \n'.format(str(time), '[{}]'.format(log_type), msg))
    f.close()


def error(msg: str):
    log_type = 'error'
    write_log(msg, log_type)


def warn(msg: str):
    log_type = 'warn'
    write_log(msg, log_type)


def info(msg: str):
    log_type = 'info'
    write_log(msg, log_type)

