from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def cancel(self):
        self._timer.cancel()
        self.is_running = False

class EventTimer(object):
    def __init__(self, interval, function,  repeated=True, *args, **kwargs):
        if repeated:
            self.thread = RepeatedTimer(interval, function, *args, **kwargs)
        else:
            self.thread = Timer(interval, function, *args, **kwargs)
            self.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()