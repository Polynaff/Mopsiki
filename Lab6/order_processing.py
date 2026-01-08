DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21

COUPON_SAVE10 = "SAVE10"
COUPON_SAVE20 = "SAVE20"
COUPON_VIP = "VIP"

SAVE10_RATE = 0.10
SAVE20_RATE_HIGH = 0.20
SAVE20_RATE_LOW = 0.05
SAVE20_THRESHOLD = 200

VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100


def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency


def _require_not_none(value, message: str):
    if value is None:
        raise ValueError(message)
    return value


def _validate_items(items: list):
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")


def _subtotal(items: list) -> int:
    return sum(item["price"] * item["qty"] for item in items)


def _discount(subtotal: int, coupon: str | None) -> int:
    if not coupon:
        return 0

    if coupon == COUPON_SAVE10:
        return int(subtotal * SAVE10_RATE)

    if coupon == COUPON_SAVE20:
        rate = SAVE20_RATE_HIGH if subtotal >= SAVE20_THRESHOLD else SAVE20_RATE_LOW
        return int(subtotal * rate)

    if coupon == COUPON_VIP:
        return VIP_DISCOUNT_HIGH if subtotal >= VIP_THRESHOLD else VIP_DISCOUNT_LOW

    raise ValueError("unknown coupon")


def _tax(amount: int) -> int:
    return int(amount * TAX_RATE)


def _order_id(user_id, items_count: int) -> str:
    return f"{user_id}-{items_count}-X"


def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)

    _require_not_none(user_id, "user_id is required")
    _require_not_none(items, "items is required")

    if currency is None:
        currency = DEFAULT_CURRENCY

    _validate_items(items)

    subtotal = _subtotal(items)
    discount = _discount(subtotal, coupon)

    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0

    tax = _tax(total_after_discount)
    total = total_after_discount + tax

    return {
        "order_id": _order_id(user_id, len(items)),
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
