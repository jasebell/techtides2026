import threading
import unittest
from datetime import datetime, timedelta, timezone

from coupons_fixed import (AlreadyRedeemed, Coupon, CouponError, CouponRepo,
                           ExpiredCoupon, UnknownCoupon, redeem)

NOW = datetime(2026, 11, 2, 9, 0, tzinfo=timezone.utc)


def make_repo(**overrides):
    repo = CouponRepo()
    fields = dict(code="LAUNCH20", percent_off=20,
                  expires_at=NOW + timedelta(days=7))
    fields.update(overrides)
    repo.add(Coupon(**fields))
    return repo


class RedeemTests(unittest.TestCase):
    def test_valid_code_applies_discount(self):
        repo = make_repo()
        self.assertEqual(redeem(repo, "LAUNCH20", "alice", 5000, now=NOW), 4000)

    def test_discount_rounds_down_to_whole_cent(self):
        repo = make_repo(percent_off=15)
        self.assertEqual(redeem(repo, "LAUNCH20", "alice", 999, now=NOW), 849)

    def test_code_is_marked_redeemed(self):
        repo = make_repo()
        redeem(repo, "LAUNCH20", "alice", 5000, now=NOW)
        self.assertEqual(repo.get("LAUNCH20").redeemed_by, "alice")

    def test_unknown_code(self):
        with self.assertRaises(UnknownCoupon):
            redeem(make_repo(), "NOPE", "alice", 5000, now=NOW)

    def test_expired_code(self):
        repo = make_repo(expires_at=NOW - timedelta(seconds=1))
        with self.assertRaises(ExpiredCoupon):
            redeem(repo, "LAUNCH20", "alice", 5000, now=NOW)

    def test_second_redemption_is_rejected(self):
        repo = make_repo()
        redeem(repo, "LAUNCH20", "alice", 5000, now=NOW)
        with self.assertRaises(AlreadyRedeemed):
            redeem(repo, "LAUNCH20", "bob", 5000, now=NOW)


class ConcurrencyTests(unittest.TestCase):
    """The test the original suite was missing."""

    def test_only_one_of_many_simultaneous_redemptions_wins(self):
        users = 50
        repo = make_repo()
        barrier = threading.Barrier(users)
        winners, rejected = [], []

        def click(user_id):
            barrier.wait()
            try:
                redeem(repo, "LAUNCH20", user_id, 5000, now=NOW)
                winners.append(user_id)
            except CouponError:
                rejected.append(user_id)

        threads = [threading.Thread(target=click, args=(f"user{i}",))
                   for i in range(users)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(winners), 1)
        self.assertEqual(len(rejected), users - 1)
        self.assertEqual(repo.get("LAUNCH20").redeemed_by, winners[0])


if __name__ == "__main__":
    unittest.main()
