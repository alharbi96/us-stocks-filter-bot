
# -*- coding: utf-8 -*-
from datetime import datetime, time
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

def now_et():
    return datetime.now(tz=ET)

def parse_hhmm(s: str) -> time:
    h, m = [int(x) for x in s.split(":")]
    return time(hour=h, minute=m, tzinfo=ET)

def current_session(pre_start="04:00", reg_start="09:30", reg_end="16:00", after_end="20:00"):
    """
    يحدد الجلسة الحالية بتوقيت نيويورك (ET).
    يرجع واحدة من: 'pre', 'regular', 'after', 'closed'
    """
    t = now_et().time()
    pre = parse_hhmm(pre_start)
    reg_s = parse_hhmm(reg_start)
    reg_e = parse_hhmm(reg_end)
    aft_e = parse_hhmm(after_end)

    if pre <= t < reg_s:
        return "pre"
    if reg_s <= t < reg_e:
        return "regular"
    if reg_e <= t < aft_e:
        return "after"
    return "closed"
