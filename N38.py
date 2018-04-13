
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class Time():

    __slots__ = '_hour', '_minute', '_second'

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    def _cmperror(x, y):
        x_ = type(x).__name__
        y_ = type(y).__name__
        raise TypeError(f"can't compare {x_} to {y_}")

    @staticmethod
    def _format_time(hh, mm, ss, timespec='auto'):
        other = ''
        if timespec == 'ampm':
            if hh <= 12:
                other = 'a.m.'
            else:
                hh = hh - 12
                other = 'p.m.'
        specs = {
            'hours': '{:02d}',
            'minutes': '{:02d}:{:02d}',
            'seconds': '{:02d}:{:02d}:{:02d}',
            'text': '{:02d} hour {:02d} min {:02d} sec',
            'ampm': '{:02d}:{:02d}:{:02d} ' + f'{other}'
        }

        if timespec == 'auto':
            timespec = 'seconds'
        try:
            fmt = specs[timespec]
        except KeyError:
            raise ValueError('Unknown timespec value')
        else:
            return fmt.format(hh, mm, ss)

    @staticmethod
    def _check_int_field(value):
        if isinstance(value, int):
            return value
        if not isinstance(value, float):
            try:
                value = value.__int__()
            except AttributeError:
                pass
            else:
                if isinstance(value, int):
                    return value
                raise TypeError(
                    f'__int__ returned non-int (type {type(value).__name__})')

            raise TypeError(
                f'an integer is required (got type {type(value).__name__})')
        raise TypeError('integer argument expected, got float')

    @staticmethod
    def _check_time_fields(hour, minute, second):
        hour = Time._check_int_field(hour)
        minute = Time._check_int_field(minute)
        second = Time._check_int_field(second)
        if not 0 <= hour <= 23:
            raise ValueError('hour must be in 0..23', hour)
        if not 0 <= minute <= 59:
            raise ValueError('minute must be in 0..59', minute)
        if not 0 <= second <= 59:
            raise ValueError('second must be in 0..59', second)
        return hour, minute, second

    def delta(self, other):
        assert isinstance(other, Time)
        s_ss = self._hour * 60 * 24 + self._minute * 60 + self._second
        o_ss = other._hour * 60 * 24 + other._minute * 60 + other._second
        result = s_ss - o_ss if s_ss >= o_ss else o_ss - s_ss
        new_hh = result // (60 * 24)
        new_mm = (result - 60 * 24 * new_hh) // 60
        new_ss = (result - 60 * 24 * new_hh - new_mm * 60)
        return Time(new_hh, new_mm, new_ss)

    def _cmp(self, other, allow_mixed=False):
        assert isinstance(other, Time)
        return _cmp((self._hour, self._minute, self._second),
                    (other._hour, other._minute, other._second))

        if allow_mixed:
            return 2  # arbitrary non-zero value
        else:
            raise TypeError("cannot compare naive and aware times")
        myhhmm = self._hour * 60 + self._minute
        othhmm = other._hour * 60 + other._minute
        return _cmp((myhhmm, self._second),
                    (othhmm, other._second))

    def __new__(cls, hour=0, minute=0, second=0):
        hour, minute, second = Time._check_time_fields(hour, minute, second)
        self = object.__new__(cls)
        self._hour = hour
        self._minute = minute
        self._second = second
        return self

    def __eq__(self, other):
        if isinstance(other, Time):
            return self._cmp(other, allow_mixed=True) == 0
        else:
            return False

    def __le__(self, other):
        if isinstance(other, Time):
            return self._cmp(other) <= 0
        else:
            Time._cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, Time):
            return self._cmp(other) < 0
        else:
            Time._cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, Time):
            return self._cmp(other) >= 0
        else:
            Time._cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, Time):
            return self._cmp(other) > 0
        else:
            Time._cmperror(self, other)

    def __str__(self, timespec='auto'):
        return Time._format_time(
            self._hour,
            self._minute,
            self._second,
            timespec)


if __name__ is '__name__':
    T1 = Time(22, 20, 59)
    T2 = Time(7, 10, 20)
    T3 = Time(7, 10, 20)

    print(f"T1 = {T1.__str__('ampm')}")
    print(f"T2 = {T2.__str__('seconds')}")
    print(f"T3 = {T3.__str__('text')}")
    print('\n')
    print(f'T1 == T2 = {T1 == T2}')
    print(f'T3 == T2 = {T3 == T2}')
    print(f'T1 > T2 = {T1 > T2}')
    print(f'T1 < T2 = {T1 < T2}')
    print(f'T1 <= T2 = {T1 <= T2}')
    print(f'T3 <= T2 = {T3 <= T2}')
    print(f'T1 >= T2 = {T1 >= T2}')
    print('\n')
    print(f'Delta T1 & T2 = {T1.delta(T2)}')
    print(f'Delta T3 & T1 = {T3.delta(T1)}')
    print(f'Delta T3 & T3 = {T3.delta(T3)}')
