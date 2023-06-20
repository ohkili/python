import time
def present_time_str():
    present_time_str = str( time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return present_time_str