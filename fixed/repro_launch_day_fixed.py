"""Launch day again, against the fixed code: 50 people click 'Apply' at once."""
import threading
from datetime import datetime, timedelta, timezone

from coupons_fixed import Coupon, CouponError, CouponRepo, redeem

USERS = 50
repo = CouponRepo()
repo.add(Coupon("LAUNCH20", 20, datetime.now(timezone.utc) + timedelta(days=7)))

barrier = threading.Barrier(USERS)
winners, rejected = [], []


def click(user_id):
    barrier.wait()  # everyone hits Apply together
    try:
        redeem(repo, "LAUNCH20", user_id, 5000)
        winners.append(user_id)
    except CouponError:
        rejected.append(user_id)


threads = [threading.Thread(target=click, args=(f"user{i}",)) for i in range(USERS)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Coupon is one-time-use. Redeemed successfully by: {len(winners)} users")
print(f"Rejected: {len(rejected)}")
print(f"Database says the owner is: {repo.get('LAUNCH20').redeemed_by}")
