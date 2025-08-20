from datetime import datetime
from zoneinfo import ZoneInfo

from sla.sla_checker import check_sla, SLAResult

TZ = ZoneInfo("Europe/Moscow")


def dt(year, month, day, hour, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=TZ)


def test_within_two_hours_ok():
    created = dt(2024, 4, 1, 9, 0)
    now = dt(2024, 4, 1, 9, 30)
    result = check_sla(created, now)
    assert result == SLAResult(status="ok", minutes=30)


def test_warn_one_hour():
    created = dt(2024, 4, 1, 9, 0)
    now = dt(2024, 4, 1, 10, 0)
    result = check_sla(created, now)
    assert result == SLAResult(status="warn_1h", minutes=60)


def test_warn_thirty_minutes():
    created = dt(2024, 4, 1, 9, 0)
    now = dt(2024, 4, 1, 10, 30)
    result = check_sla(created, now)
    assert result == SLAResult(status="warn_30m", minutes=90)


def test_violation_after_two_hours():
    created = dt(2024, 4, 1, 9, 0)
    now = dt(2024, 4, 1, 11, 0)
    result = check_sla(created, now)
    assert result == SLAResult(status="violation", minutes=120)


def test_excludes_weekend():
    created = dt(2024, 4, 5, 17, 0)  # Friday
    now = dt(2024, 4, 8, 9, 30)  # Monday
    result = check_sla(created, now)
    # 60 minutes on Friday evening + 30 minutes on Monday morning
    assert result == SLAResult(status="warn_30m", minutes=90)
