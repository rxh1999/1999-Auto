import time

INFINITE_LOOP_MAX_COUNT = 15



def try_limited_sleep(sleep_seconds: float, break_condition, limit_cnt):
    return do_try_limited(lambda: time.sleep(sleep_seconds), break_condition, limit_cnt)


def try_limited(do_func, break_condition):
    return do_try_limited(do_func, break_condition, INFINITE_LOOP_MAX_COUNT)
def do_try_limited(do_func, break_condition, limit_cnt):
    while_cnt = limit_cnt
    while (while_cnt > 0):
        do_func()
        if break_condition():
            break
        while_cnt -= 1
    return while_cnt > 0

