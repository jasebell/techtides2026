"""One-time coupon redemption (fixed: atomic claim)."""
import threading
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional


class CouponError(Exception):
    pass


class UnknownCoupon(CouponError):
    pass


class ExpiredCoupon(CouponError):
    pass


class AlreadyRedeemed(CouponError):
    pass


@dataclass
class Coupon:
    code: str
    percent_off: int
    expires_at: datetime
    redeemed_by: Optional[str] = None


class CouponRepo:
    """Stand-in for the database. The sleep is the network round-trip."""

    def __init__(self):
        self._rows = {}
        self._lock = threading.Lock()  # protects the dict itself

    def add(self, coupon: Coupon) -> None:
        with self._lock:
            self._rows[coupon.code] = replace(coupon)

    def get(self, code: str) -> Optional[Coupon]:
        time.sleep(0.01)
        with self._lock:
            row = self._rows.get(code)
            return replace(row) if row else None

    def claim(self, code: str, user_id: str) -> bool:
        """Atomically mark the coupon as redeemed. True only for the one winner.

        In a real database this is a single statement:
            UPDATE coupons SET redeemed_by = :user
            WHERE code = :code AND redeemed_by IS NULL
        and you check the affected row count.
        """
        time.sleep(0.01)
        with self._lock:  # check and write happen under ONE lock
            row = self._rows.get(code)
            if row is None or row.redeemed_by is not None:
                return False
            row.redeemed_by = user_id
            return True


def redeem(repo: CouponRepo, code: str, user_id: str, price_cents: int,
           now: Optional[datetime] = None) -> int:
    """Redeem a one-time coupon and return the discounted price in cents."""
    now = now or datetime.now(timezone.utc)

    coupon = repo.get(code)
    if coupon is None:
        raise UnknownCoupon(code)
    if coupon.redeemed_by is not None:
        raise AlreadyRedeemed(code)
    if coupon.expires_at < now:
        raise ExpiredCoupon(code)

    # The checks above are only a fast path. This is the real gate.
    if not repo.claim(code, user_id):
        raise AlreadyRedeemed(code)

    return price_cents * (100 - coupon.percent_off) // 100
