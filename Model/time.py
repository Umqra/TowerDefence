__author__ = 'umqra'


class Time:
    _hours = 24
    _minutes = 60
    _seconds = 60
    _total_seconds = _hours * _minutes * _seconds
    _seconds_in_hour = _minutes * _seconds

    def __init__(self, value=0):
        self.value = value % Time._total_seconds
        self.day = int(value // Time._total_seconds)
        self._coefficient = 2000

    @staticmethod
    def max_total_seconds():
        return Time._total_seconds

    @staticmethod
    def seconds_in_hour():
        return Time._seconds_in_hour

    @property
    def hour(self):
        return self.value // (Time._minutes * Time._seconds)

    @property
    def total_hours(self):
        return int(self.hour + self.day * Time._total_seconds)

    @property
    def minutes(self):
        return (self.value // Time._seconds) % 60

    @property
    def seconds(self):
        return self.value % 60

    def get_cur_seconds(self):
        return self.day * Time._total_seconds + self.value

    @staticmethod
    def fromDHMS(day, h, m, s):
        result = Time.fromHMS(h, m, s)
        result.day = day
        return result

    @staticmethod
    def fromHMS(h, m, s):
        return Time(h * Time._minutes * Time._seconds +
                    m * Time._seconds +
                    s)

    def __str__(self):
        return "{} day. {}:{}:{}".format(self.day, self.hour, self.minutes, self.seconds)

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

    def __sub__(self, other):
        return Time(self.get_cur_seconds() - other.get_cur_seconds())

    def time_faster(self, times):
        self._coefficient *= times

    def time_slower(self, times):
        self._coefficient /= times

    def tick(self, dt):
        self.value += dt * self._coefficient
        if self.value >= Time._total_seconds:
            self.day += 1
            self.value -= Time._total_seconds