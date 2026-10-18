# Spec: one-time coupon redemption

Prompt given to Claude:

> Add a `redeem(code, user_id, price_cents)` function for our launch coupons.
> Each code can be used once, by one user. Codes expire. Return the discounted
> price in cents. Raise clear errors for unknown, expired, or already-used codes.
> Add tests.

Acceptance criteria:
- Unknown code -> `UnknownCoupon`
- Expired code -> `ExpiredCoupon`
- Code already redeemed -> `AlreadyRedeemed`
- Valid code -> price reduced by `percent_off`, rounded down to a whole cent
- Code is marked as redeemed by `user_id`
