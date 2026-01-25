import unittest

from game.fnaacm.timer import Timer


class TestTimer(unittest.TestCase):
    def setUp(self) -> None:
        self.__duration = 1
        self.timer = Timer(self.__duration)
        self.n = 67
        
    def test_state_over_time(self):
        assert self.timer.done
        self.timer.reset()
        for i in range(self.__duration):
            assert not self.timer.done
            self.timer.tick()
            if i == self.__duration:
                assert self.timer.done

    def test_formula(self):
        n = self.n
        self.timer.reset(force=True)
        for _ in range(self.timer.duration):
            self.timer.tick()
            n += 1
        assert n == self.n + self.timer.duration

