
# -*- coding: utf-8 -*-
from typing import Tuple
from config import (
    PRICE_MIN, PRICE_MAX, RVOL_MIN,
    DOLLAR_5M_MIN_REG, DOLLAR_5M_MIN_EXT,
    VOLUME_5M_MIN, VOLUME_5M_MIN_SUB1,
    CHANGE_5M_MIN_MOMENTUM, CHANGE_5M_MIN_HOD,
    OPENING_DRIVE_CHANGE_MIN, OPENING_DRIVE_MULT_VOL,
)
from sessions import current_session

def session_thresholds(session: str) -> Tuple[float, int]:
    dollar_min = DOLLAR_5M_MIN_REG if session == "regular" else DOLLAR_5M_MIN_EXT
    vol_min = VOLUME_5M_MIN
    return dollar_min, vol_min

def base_checks(price: float, day_volume: int, avg_volume_20d: int, rvol: float) -> bool:
    if not (PRICE_MIN <= price <= PRICE_MAX):
        return False
    if avg_volume_20d <= 0:
        return False
    if rvol < RVOL_MIN:
        return False
    return True

def dynamic_min_volume_5m(price: float, default_min: int) -> int:
    # إذا السعر أقل من 1$، نرفع الحد الأدنى للحجم
    return VOLUME_5M_MIN_SUB1 if price < 1.0 else default_min

def trigger_hod(is_hod_break: bool, chg5m: float, vol5m: int, avg5m20: float | None) -> bool:
    if not is_hod_break:
        return False
    if chg5m < CHANGE_5M_MIN_HOD:
        return False
    if avg5m20 and vol5m < 1.5 * avg5m20:
        return False
    return True

def trigger_momentum(chg5m: float) -> bool:
    return chg5m >= CHANGE_5M_MIN_MOMENTUM

def trigger_opening_drive(is_regular: bool, minutes_from_open: int, chg_from_open: float, vol5m: int, avg5m20: float | None) -> bool:
    if not is_regular:
        return False
    if minutes_from_open not in (0, 5):  # أول شمعتين (0-5 و 5-10)
        return False
    if chg_from_open < OPENING_DRIVE_CHANGE_MIN:
        return False
    if avg5m20 and vol5m < OPENING_DRIVE_MULT_VOL * avg5m20:
        return False
    return True
