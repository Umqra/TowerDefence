__author__ = 'umqra'


class Time:
    hours = 24
    minutes = 60
    seconds = 60
    total_seconds = hours * minutes * seconds

    def __init__(self, value=0):
        self.value = value
        self._coefficient = 2000

    @staticmethod
    def fromHMS(h, m, s):
        return Time(h * Time.minutes * Time.seconds +
                    m * Time.seconds +
                    s)

    def time_faster(self, times):
        self._coefficient *= times

    def time_slower(self, times):
        self._coefficient /= times

    def tick(self, dt):
        self.value += dt * self._coefficient
        self.value %= Time.total_seconds