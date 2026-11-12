"""State handles bound to the authenticated user. The user ID comes from the
verified token, never from a tool argument."""
import secrets

baskets = {}


def create_basket(user_id):
    handle = "bsk_" + secrets.token_urlsafe(16)
    baskets[(user_id, handle)] = []
    return handle


def add_item(user_id, handle, sku):
    basket = baskets.get((user_id, handle))
    if basket is None:
        return {"isError": True, "text": "Unknown or expired basket. Create a new one."}
    basket.append(sku)
    return {"isError": False, "text": f"Added {sku}. Basket holds {len(basket)} item(s)."}


if __name__ == "__main__":
    handle = create_basket("user-17")
    print("handle length:", len(handle))
    print("owner:", add_item("user-17", handle, "SKU-1"))
    print("other user, same handle:", add_item("user-99", handle, "SKU-1"))
