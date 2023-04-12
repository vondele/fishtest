import time

def log_timer(wrapped):
    def wrapper(context, request):
        start = time.time()
        response = wrapped(context, request)
        duration = time.time() - start
        print('route %s took %.6f seconds' %(request.matched_route.name, duration))
        return response
    return wrapper
