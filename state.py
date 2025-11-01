
# -*- coding: utf-8 -*-
import time
from collections import defaultdict
from config import DEDUP_WINDOW_SEC

class DayState:
    def __init__(self):
        self.last_alert_ts = {}          # symbol -> ts
        self.alert_count = defaultdict(int)  # symbol -> count

    def should_notify(self, symbol: str) -> bool:
        now = time.time()
        last = self.last_alert_ts.get(symbol, 0)
        if now - last >= DEDUP_WINDOW_SEC:
            self.last_alert_ts[symbol] = now
            self.alert_count[symbol] += 1
            return True
        return False

    def count(self, symbol: str) -> int:
        return self.alert_count[symbol]

    def reset_daily(self):
        self.last_alert_ts.clear()
        self.alert_count.clear()
