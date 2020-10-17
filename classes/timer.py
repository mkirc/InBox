from time import perf_counter

class TimerError(Exception):
    """custom Timer exception"""

class Timer():

    def __init__(self):

        self._startTime = None

    def start(self):

        if self._startTime != None:
            raise TimerError(f'Timer is running, use stop() to stop it.')
        else:
            self._startTime = perf_counter()

    def stop(self):

        if self._startTime = None:
            raise TimerError(f'Timer is not running, use start() to start it.')
        else:

            elapsedTime = perf_counter() - self._startTime
            
            print('Elapsed Time: %0.4f seconds.' % (elapsedTime))

            self._startTime = None

            return elapsedTime


