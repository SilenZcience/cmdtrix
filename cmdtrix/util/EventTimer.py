from threading import Timer
from pynput import keyboard

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

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

class KeyboardListener():
    def __init__(self, on_press=None, on_release=None, *args, **kwargs):
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        
    def start(self):
        self.listener.start()
        
    def cancel(self):
        self.listener.stop()

class EventTimer(object):
    def __init__(self, interval, function, type="repeatingTimer", *args, **kwargs):
        options = ['repeatingTimer', 'Timer', 'keyboardListener']
        if type == options[0]:
            self.thread = RepeatedTimer(interval, function, *args, **kwargs)
        elif type == options[1]:
            self.thread = Timer(interval, function, *args, **kwargs)
        elif type == options[2]:
            self.thread = KeyboardListener(*args, **kwargs)
        else:
            raise ValueError('Allowed are only the following options: ' + ','.join(options))
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()