import threading
import traceback

from game.common.enums import ActionType


class Thread(threading.Thread):
    """
    `Thread Class Notes:`
        Threads are how the engine communicates with user clients. These Threads are built to catch errors. If an error
        is caught, it will be logged, but the program will continue to run.

        If multithreading is needed for whatever reason, this class would be used for that.
    """
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func
        self.result: list[ActionType] = []
        self.error = None

    def run(self):
        try:
            self.result = self.func(*self.args)
        except Exception:
            self.error = traceback.format_exc()


class CommunicationThread(Thread):
    """
    `Communication Thread Class Notes:`

        Communication Threads are bulkier than normal Threads. It also has error catching functionality, but tends
        to be used for single-use, single-variable communication.

        For example, if a client tries to use malicious code in any methods, a Communication Thread is used to check
        any given parameters and throw an error if the type needed does not match what is given.

        Communication Threads use a nested class to make the return value of the Communication Thread private. It helps
        to keep things secure. This is now achieved through getter and setter decorators. Since the code here was
        written long ago, the structure is different. For future note, use getter and setter decorators as needed.
    """
    def __init__(self, func, args=None, variable_type=None):
        super().__init__(func, args)
        self.type = variable_type

        class InternalObject:
            def __init__(self):
                self.value = None

        self.safeObject = InternalObject()

    def run(self):
        try:
            self.safeObject.value = self.func(*self.args)
        except Exception:
            self.error = traceback.format_exc()

        if self.type is not None and not isinstance(self.safeObject.value, self.type):
            self.safeObject.value = None

    def retrieve_value(self):
        return self.safeObject.value

