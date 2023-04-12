import time

def log_timer(wrapped):
    def wrapper(context, request):
        start = time.time()
        response = wrapped(context, request)
        duration = time.time() - start
        print('view %s took %.6f seconds' %(wrapped.__name__, duration))
        return response
    return wrapper
