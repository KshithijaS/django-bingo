from django.utils import timezone
from django.conf import settings

import pytz
from datetime import datetime

# Time range, in which a game can be started. None = no limit
# or a ((Hour, Minute), (Hour, Minute)) tuple defining the range.
GAME_START_TIMES = getattr(settings, "GAME_START_TIMES", None)

# Time, after which a running game is ended. Has only effect, if
# GAME_START_TIMES is set, and needs to be outside of GAME_START_TIMES.
# Values: tuple (hour, minute) or None for no restriction
GAME_END_TIME = getattr(settings, "GAME_END_TIME", None)


def get_times():
    now = timezone.get_current_timezone().normalize(timezone.now())
    if GAME_START_TIMES:
        start, end = GAME_START_TIMES
        start_time_start = now.replace(
            hour=start[0], minute=start[1], second=0, microsecond=0)
        start_time_end = now.replace(
            hour=end[0], minute=end[1], second=0, microsecond=0)
    else:
        start_time_start = None
        start_time_end = None
    if GAME_END_TIME:
        end = GAME_END_TIME
        end_time = now
        end_time = end_time.replace(
            hour=end[0], minute=end[1], second=0, microsecond=0)
        if start_time_end is not None and end_time < start_time_end:
            end_time = end_time + timezone.timedelta(1, 0)
    else:
        end_time = None

    return now, start_time_start, start_time_end, end_time


def is_starttime():
    if GAME_START_TIMES is None:
        return True
    else:
        now, start_time_start, start_time_end, end_time = get_times()
        if start_time_end > start_time_start:
            return start_time_start < now < start_time_end
        else:
            # to check if its inside a interval between two days,
            # check if its *not* in the interval between
            # end and the *next* start
            return not (start_time_end < now < start_time_start)


def is_after_endtime():
    if GAME_END_TIME is None or is_starttime():
        return False
    else:
        now, start_time_start, start_time_end, end_time = get_times()
        end = GAME_END_TIME
        # game starts today and ends today
        if start_time_end < end_time:
            return not (start_time_end < now < end_time)
        else:
            # time is between end_time and *next* start time
            return end_time < now < start_time_start
