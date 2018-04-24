class Time():

    __slots__ = '_hour', '_minute', '_second'

    @property
    def times_of_day(self):
        NIGHT_1 = Time(0,0,1)
        NIGHT_2 = Time(6,0)

        MORNING_1 = Time(6,0,1)
        MORNING_2 = Time(12,0)

        DAY_1 = Time(12,0,1)
        DAY_2 = Time(18,0)

        EVENING_1 = Time(18,0,1)
        EVENING_2 = Time(0,0)

        if self > NIGHT_1 and self < NIGHT_2:
            return "NIGHT"
        elif self > MORNING_1  and self < MORNING_2:
            return "MORNING"
        elif self > DAY_1  and self < DAY_2:
            return "DAY"
        elif self > EVENING_1:
            return "EVENING"

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

    @staticmethod
    def _global_cmp(x, y):
        return 0 if x == y else 1 if x > y else -1

    def delta(self, other):
        assert isinstance(other, Time)
        s_ss = self._hour * 60 * 24 + self._minute * 60 + self._second
        o_ss = other._hour * 60 * 24 + other._minute * 60 + other._second
        result = s_ss - o_ss if s_ss >= o_ss else o_ss - s_ss
        new_hh = result // (60 * 24)
        new_mm = (result - 60 * 24 * new_hh) // 60
        new_ss = (result - 60 * 24 * new_hh - new_mm * 60)
        return Time(new_hh, new_mm, new_ss)

    def _cmp(self, other):
        assert isinstance(other, Time)
        return Time._global_cmp((self._hour, self._minute, self._second),
                    (other._hour, other._minute, other._second))

    def __new__(cls, hour=0, minute=0, second=0):
        hour, minute, second = Time._check_time_fields(hour, minute, second)
        self = object.__new__(cls)
        self._hour = hour
        self._minute = minute
        self._second = second
        return self

    def __eq__(self, other):
        if isinstance(other, Time):
            return self._cmp(other) == 0
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

if __name__ is '__main__':
    T1 = Time(22, 20, 59)
    T2 = Time(7, 10, 20)
    T3 = Time(7, 10, 20)

    T4 = Time(12, 10, 13)
    T5 = Time(5, 50, 0)

    print(f"T1 = {T1.__str__('ampm')}")
    print(f"T2 = {T2.__str__('seconds')}")
    print(f"T3 = {T3.__str__('text')}")
    print(f"T4 = {T4.__str__('seconds')}")
    print(f"T5 = {T5.__str__('seconds')}")
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
    print('\n')
    print(f'Time of day T1 = {T1.times_of_day}')
    print(f'Time of day T2 = {T2.times_of_day}')
    print(f'Time of day T3 = {T3.times_of_day}')
    print(f'Time of day T4 = {T4.times_of_day}')
    print(f'Time of day T5 = {T5.times_of_day}')
