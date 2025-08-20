from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

# Constants for working hours
WORK_START = time(9, 0)
WORK_END = time(18, 0)
TIMEZONE = ZoneInfo("Europe/Moscow")


@dataclass
class SLAResult:
    """Result of SLA check."""

    status: str
    minutes: int


def _business_minutes(start: datetime, end: datetime) -> int:
    """Return minutes between datetimes during business hours only.

    Business hours: Monday-Friday, 09:00-18:00 Europe/Moscow.
    """
    if end <= start:
        return 0

    tz = TIMEZONE
    start = start.astimezone(tz)
    end = end.astimezone(tz)

    minutes = 0
    current = start
    one_day = timedelta(days=1)

    while current.date() <= end.date():
        day_start = datetime.combine(current.date(), WORK_START, tz)
        day_end = datetime.combine(current.date(), WORK_END, tz)

        # intersection of [day_start, day_end) with [start, end)
        interval_start = max(day_start, start)
        interval_end = min(day_end, end)

        if interval_start < interval_end and day_start.weekday() < 5:
            minutes += int((interval_end - interval_start).total_seconds() // 60)

        current = datetime.combine((current + one_day).date(), time(0, 0), tz)

    return minutes


def check_sla(created_at: datetime, now: datetime | None = None) -> SLAResult:
    """Check SLA status for ticket created at ``created_at``.

    ``now`` defaults to current time. Returns ``SLAResult`` with status:
    - "ok" – SLA within limits
    - "warn_1h" – 1 hour left
    - "warn_30m" – 30 minutes left
    - "violation" – SLA violated
    """

    if now is None:
        now = datetime.now(TIMEZONE)

    minutes = _business_minutes(created_at, now)

    if minutes >= 120:
        status = "violation"
    elif minutes >= 90:
        status = "warn_30m"
    elif minutes >= 60:
        status = "warn_1h"
    else:
        status = "ok"

    return SLAResult(status=status, minutes=minutes)
