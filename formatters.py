
# -*- coding: utf-8 -*-
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

SUFFIXES = [
    (1_000_000_000_000, "T"),
    (1_000_000_000, "B"),
    (1_000_000, "M"),
    (1_000, "K"),
]

def human_num(n: float, currency=False) -> str:
    try:
        n = float(n)
    except Exception:
        return str(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    for thresh, suf in SUFFIXES:
        if n >= thresh:
            val = n / thresh
            s = f"{val:.2f}".rstrip("0").rstrip(".")
            return f"{sign}${s}{suf}" if currency else f"{sign}{s}{suf}"
    s = f"{n:.0f}"
    return f"{sign}${s}" if currency else f"{sign}{s}"

def human_pct(x: float) -> str:
    return f"{x:+.2f}%"

def now_et_str() -> str:
    return datetime.now(tz=ET).strftime("%I:%M %p ET").lstrip("0")

def compose_message(
    symbol: str,
    move_type: str,
    alert_count: int,
    pct_day: float,
    pct_5m: float,
    price: float,
    free_float: float | None,
    shares_out: float | None,
    mcap: float | None,
    rvol: float,
    first5m_volume: int | None,
    dollar_5m: float,
):
    float_disp = None
    if free_float and free_float > 0:
        float_disp = human_num(free_float)
    elif shares_out and shares_out > 0:
        float_disp = human_num(shares_out)

    lines = [
        f"▪️ الرمز: {symbol}",
        f"▪️ نوع الحركة: {move_type}",
        f"▪️ عدد مرات التنبيه اليوم: {alert_count}",
        f"▪️ نسبة الارتفاع: {human_pct(pct_day)} (اليوم) | {human_pct(pct_5m)} (آخر 5د)",
        f"▪️ السعر الحالي: {human_num(price, currency=True)}",
        f"▪️ عدد الأسهم المتاحة للتداول: {float_disp if float_disp else '—'}",
        f"▪️ القيمة السوقية: {human_num(mcap, currency=True) if mcap else '—'}",
        f"▪️ الحجم النسبي: {rvol:.2f}×",
        f"▪️ حجم أول دقيقة: {human_num(first5m_volume) if first5m_volume is not None else '—'}",
        f"▪️ حجم السيولة: {human_num(dollar_5m, currency=True)} (آخر 5د)",
        f"🇺🇸 التوقيت الأمريكي: {now_et_str()}",
    ]
    return "\n".join(lines)
