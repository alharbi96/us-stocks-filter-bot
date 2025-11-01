# -*- coding: utf-8 -*-
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    POLL_INTERVAL_SEC, RVOL_MIN, PRICE_MIN, PRICE_MAX,
    PREPOST_MIN_VOLUME_5M, PREPOST_MIN_DOLLAR_5M,
)
from sessions import current_session, now_et
from market import load_market_client
from filters import (
    session_thresholds, base_checks, dynamic_min_volume_5m,
    trigger_hod, trigger_momentum, trigger_opening_drive
)
from state import DayState
from formatters import compose_message
from bot import send_text

ET = ZoneInfo("America/New_York")

def get_time_with_zone() -> str:
    """يعرض الوقت الحالي في التوقيت الأمريكي مع تحديد (EDT أو EST)."""
    dt = datetime.now(ET)
    is_dst = bool(dt.dst())
    tz_name = "EDT" if is_dst else "EST"
    return f'{dt.strftime("%I:%M %p")} {tz_name}'

def compute_rvol(day_volume: int, avg20: int) -> float:
    if avg20 <= 0:
        return 0.0
    return day_volume / float(avg20)

def minutes_from_open_et(dt: datetime) -> int:
    d = dt.astimezone(ET)
    open_dt = d.replace(hour=9, minute=30, second=0, microsecond=0)
    delta = d - open_dt
    return int(delta.total_seconds() // 60)

def run():
    client = load_market_client()
    state = DayState()
    last_day = now_et().date()

    print(f"Starting bot. Price range: ${PRICE_MIN}–${PRICE_MAX}, RVOL>={RVOL_MIN}")

    while True:
        try:
            today = now_et().date()
            if today != last_day:
                state.reset_daily()
                last_day = today

            session = current_session()
            is_regular = session == "regular"
            dollar_min, vol_min_default = session_thresholds(session)

            symbols = client.list_candidates()
            snaps = client.fetch_snapshot(symbols)

            for snap in snaps:
                rvol = compute_rvol(snap.day_volume, snap.avg_volume_20d)
                if not base_checks(snap.price, snap.day_volume, snap.avg_volume_20d, rvol):
                    continue

                m5 = client.fetch_intraday_5m(snap.symbol)
                vol_min = dynamic_min_volume_5m(snap.price, vol_min_default)

                # حدود السيولة الأساسية
                if m5.dollar_5m < dollar_min:
                    continue
                if m5.volume_5m < vol_min:
                    continue

                # ⚙️ فلتر إضافي للجلسات خارج السوق الرسمية
                if not is_regular:
                    if (m5.volume_5m < PREPOST_MIN_VOLUME_5M) or (m5.dollar_5m < PREPOST_MIN_DOLLAR_5M):
                        continue

                fired = None
                if trigger_hod(m5.is_hod_break, m5.change_pct_5m, m5.volume_5m, m5.avg_vol_5m_20):
                    fired = "كسر قمة اليوم"

                if not fired and trigger_momentum(m5.change_pct_5m):
                    fired = "اندفاع لحظي"

                if not fired and is_regular:
                    mins_from_open = minutes_from_open_et(datetime.now(tz=ET))
                    if trigger_opening_drive(is_regular, mins_from_open, m5.change_pct_5m, m5.volume_5m, m5.avg_vol_5m_20):
                        fired = "اندفاعة الافتتاح"

                if not fired:
                    continue

                if not state.should_notify(snap.symbol):
                    continue
                count = state.count(snap.symbol)

                pct_day = ((snap.price - snap.prev_close) / snap.prev_close * 100.0) if snap.prev_close else 0.0

                msg = compose_message(
                    symbol=snap.symbol,
                    move_type=fired,
                    alert_count=count,
                    pct_day=pct_day,
                    pct_5m=m5.change_pct_5m,
                    price=snap.price,
                    free_float=snap.free_float,
                    shares_out=snap.shares_out,
                    mcap=snap.market_cap,
                    rvol=rvol,
                    first5m_volume=m5.first5m_volume,
                    dollar_5m=m5.dollar_5m,
                )

                msg += f"\n🇺🇸 التوقيت الأمريكي: {get_time_with_zone()}"
                send_text(msg)

        except Exception as e:
            print("Loop error:", e)

        time.sleep(POLL_INTERVAL_SEC)

if __name__ == "__main__":
    run()
