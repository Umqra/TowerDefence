__author__ = 'umqra'


class Time:
    hours = 24
    minutes = 60
    seconds = 60
    total_seconds = hours * minutes * seconds

    def __init__(self, value=0):
        self.value = value
        self.day = 0
        self._coefficient = 2000

    @staticmethod
    def fromDHMS(day, h, m, s):
        result = Time.fromHMS(h, m, s)
        result.day = day
        return result

    @staticmethod
    def fromHMS(h, m, s):
        return Time(h * Time.minutes * Time.seconds +
                    m * Time.seconds +
                    s)

    def __eq__(self, other):
        return (self.day, self.value) == (other.day, other.value)

    def __le__(self, other):
        return (self.day, self.value) <= (other.day, other.value)

    def __ge__(self, other):
        return (self.day, self.value) >= (other.day, other.value)

    def __lt__(self, other):
        return (self.day, self.value) < (other.day, other.value)

    def __gt__(self, other):
        return (self.day, self.value) > (other.day, other.value)

    def time_faster(self, times):
        self._coefficient *= times

    def time_slower(self, times):
        self._coefficient /= times

    def tick(self, dt):
        self.value += dt * self._coefficient
        if self.value >= Time.total_seconds:
            self.day += 1
            self.value -= Time.total_seconds