import time

def time_of_function(function):
    def wrapped(*args):
        start_time = time.time()
        res = function(*args)
        print("\nВремя выполнения:",round(time.time() - start_time, 2), "сек.")
        return res
    return wrapped