from bson import ObjectId

def item_helper(item):
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"].strftime("%Y-%m-%d"),
        "insert_date": item["insert_date"]
    }


def is_valid_objectid(id: str) -> bool:
    return ObjectId.is_valid(id)


def clock_in_helper(record):
    return {
        "id": str(record["_id"]),
        "email": record["email"],
        "location": record["location"],
        "insert_date": record["insert_date"]
    }