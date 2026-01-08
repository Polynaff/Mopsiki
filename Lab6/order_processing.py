DISCOUNT_COUPON = "DISCOUNT10"
DISCOUNT_RATE = 0.9


def parse_request(request: dict) -> dict:
    user_id = _get_required(request, "user_id")
    items = _get_required(request, "items")

    total = _calculate_total(items)
    total = _apply_discount(total, request.get("coupon"))

    return {"user_id": user_id, "total": total}


def _get_required(data: dict, key: str):
    value = data.get(key)
    if not value:
        raise ValueError(f"{key} required")
    return value


def _calculate_total(items: list) -> float:
    return sum(
        _item_cost(item) for item in items
    )


def _item_cost(item: dict) -> float:
    price = item.get("price", 0)
    qty = item.get("qty", 1)
    return price * qty


def _apply_discount(total: float, coupon: str | None) -> float:
    if coupon == DISCOUNT_COUPON:
        return total * DISCOUNT_RATE
    return total
