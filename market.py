
# -*- coding: utf-8 -*-
"""
طبقة مزوّد السوق:
- MarketClient: واجهة موحّدة.
- MockMarketClient: بيانات وهمية للاختبار المحلي (MARKETDATA_MOCK=true).
مطلوب منك ربط الدوال الداخلية بنقاط نهاية مزوّدك الحقيقي.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import os, random
import requests

@dataclass
class SymbolSnapshot:
    symbol: str
    price: float
    prev_close: float
    day_volume: int
    avg_volume_20d: int
    shares_out: Optional[int] = None
    free_float: Optional[int] = None
    market_cap: Optional[float] = None

@dataclass
class IntradayMetrics5m:
    change_pct_5m: float          # نسبة التغير آخر 5 د
    volume_5m: int                # حجم آخر 5 د
    dollar_5m: float              # سيولة آخر 5 د = السعر * حجم5د
    is_hod_break: bool            # هل تم كسر قمة اليوم
    avg_vol_5m_20: Optional[float]=None  # متوسط حجم 5د آخر 20 شمعة
    first5m_volume: Optional[int]=None   # حجم أول 5 د (09:30–09:35)

class MarketClient:
    def __init__(self, api_key: str="", base_url: str=""):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/") if base_url else ""

    def list_candidates(self) -> List[str]:
        """
        يرجع قائمة من التيكرات المرشحة (سعر بين 0.30 و 15) لتقليل الضغط.
        TODO: اربطها مع endpoint مناسب (screener/quotes).
        """
        raise NotImplementedError

    def fetch_snapshot(self, symbols: List[str]) -> List[SymbolSnapshot]:
        """يرجع لقطات أساسية لتيكرات محددة."""
        raise NotImplementedError

    def fetch_intraday_5m(self, symbol: str) -> IntradayMetrics5m:
        """يرجع مقاييس 5 دقائق الضرورية لسهم واحد."""
        raise NotImplementedError

# ================== Mock ==================
class MockMarketClient(MarketClient):
    universe = ["NVOS","PLTR","GME","AMC","SOFI","AI","RIVN","LCID","IONQ","CVNA","SOUN","UPST","MARA","RIOT","TQQQ","SQQQ"]

    def list_candidates(self) -> List[str]:
        import random
        picks = random.sample(self.universe, k=min(8, len(self.universe)))
        return picks

    def fetch_snapshot(self, symbols: List[str]) -> List[SymbolSnapshot]:
        out = []
        import random
        for s in symbols:
            price = round(random.uniform(0.35, 14.5), 2)
            prev = round(price * random.uniform(0.9, 1.1), 2)
            day_vol = random.randint(200_000, 20_000_000)
            avg20 = random.randint(300_000, 15_000_000)
            shares = random.randint(20_000_000, 2_000_000_000)
            mcap = price * shares
            out.append(SymbolSnapshot(
                symbol=s, price=price, prev_close=prev, day_volume=day_vol,
                avg_volume_20d=avg20, shares_out=shares, free_float=None, market_cap=mcap
            ))
        return out

    def fetch_intraday_5m(self, symbol: str) -> IntradayMetrics5m:
        import random
        price = round(random.uniform(0.35, 14.5), 2)
        vol5 = random.randint(20_000, 2_000_000)
        ch5 = random.uniform(-2.0, 3.5)
        is_hod = random.random() < 0.25
        avg5 = random.randint(50_000, 400_000)
        first5 = random.randint(50_000, 2_000_000)
        return IntradayMetrics5m(
            change_pct_5m=ch5,
            volume_5m=vol5,
            dollar_5m=price*vol5,
            is_hod_break=is_hod,
            avg_vol_5m_20=avg5,
            first5m_volume=first5,
        )

def load_market_client() -> MarketClient:
    if os.getenv("MARKETDATA_MOCK", "false").lower() == "true":
        return MockMarketClient()
    api_key = os.getenv("MARKETDATA_API_KEY", "")
    base_url = os.getenv("MARKETDATA_BASE_URL", "")
    if not api_key or not base_url:
        return MockMarketClient()
    return RealMarketClient(api_key=api_key, base_url=base_url)

class RealMarketClient(MarketClient):
    def list_candidates(self) -> List[str]:
        # TODO: اربط مع endpoint يعطي رموز ضمن نطاق السعر والحجم
        raise NotImplementedError("اربط هذه الدالة مع مزودك الحقيقي.")
    def fetch_snapshot(self, symbols: List[str]) -> List[SymbolSnapshot]:
        # TODO
        raise NotImplementedError("اربط هذه الدالة مع مزودك الحقيقي.")
    def fetch_intraday_5m(self, symbol: str) -> IntradayMetrics5m:
        # TODO
        raise NotImplementedError("اربط هذه الدالة مع مزودك الحقيقي.")
