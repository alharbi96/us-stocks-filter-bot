
# -*- coding: utf-8 -*-
"""
إعدادات البوت والقيم الافتراضية.
يمكن تعديلها عبر متغيرات البيئة عند النشر.
"""
import os

PRICE_MIN = float(os.getenv("PRICE_MIN", "0.30"))
PRICE_MAX = float(os.getenv("PRICE_MAX", "15.0"))

# سيولة 5 دقائق حسب الجلسة
DOLLAR_5M_MIN_REG = float(os.getenv("DOLLAR_5M_MIN_REG", "1500000"))   # $1.5M
DOLLAR_5M_MIN_EXT = float(os.getenv("DOLLAR_5M_MIN_EXT", "600000"))    # $0.6M (Pre/After)

# حجم آخر 5 دقائق (سهم)
VOLUME_5M_MIN = int(os.getenv("VOLUME_5M_MIN", "50000"))               # 50K
VOLUME_5M_MIN_SUB1 = int(os.getenv("VOLUME_5M_MIN_SUB1", "100000"))    # 100K إذا السعر < $1

# RVOL النسبي اليومي
RVOL_MIN = float(os.getenv("RVOL_MIN", "1.8"))

# تغير آخر 5 دقائق
CHANGE_5M_MIN_MOMENTUM = float(os.getenv("CHANGE_5M_MIN_MOMENTUM", "1.0"))   # Momentum
CHANGE_5M_MIN_HOD = float(os.getenv("CHANGE_5M_MIN_HOD", "0.6"))             # HOD

# Opening Drive (أول 10 دقائق من Regular)
OPENING_DRIVE_CHANGE_MIN = float(os.getenv("OPENING_DRIVE_CHANGE_MIN", "1.2"))
OPENING_DRIVE_MULT_VOL = float(os.getenv("OPENING_DRIVE_MULT_VOL", "3.0"))

# منع التكرار (ثواني)
DEDUP_WINDOW_SEC = int(os.getenv("DEDUP_WINDOW_SEC", "600"))   # 10 دقائق

# جلسات التداول (بتوقيت نيويورك ET)
# ملاحظة: سنستخدم هذه الأوقات كمرجع تقريبي؛ قد تختلف العطل الرسمية
PRE_START = os.getenv("PRE_START", "04:00")
REG_START = os.getenv("REG_START", "09:30")
REG_END   = os.getenv("REG_END",   "16:00")
AFTER_END = os.getenv("AFTER_END", "20:00")

# سرعة الاستطلاع (ثواني)
POLL_INTERVAL_SEC = int(os.getenv("POLL_INTERVAL_SEC", "35"))

# تفعيل الموك للاختبار المحلي
MARKETDATA_MOCK = os.getenv("MARKETDATA_MOCK", "false").lower() == "true"
