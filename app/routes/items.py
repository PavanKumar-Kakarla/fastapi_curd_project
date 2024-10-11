from fastapi import APIRouter, HTTPException, status, Query
from app.config import db
from app.models import Item
from app.utils import item_helper, is_valid_objectid
from bson import ObjectId
from datetime import datetime
from typing import Optional


router = APIRouter()

# Creating the new item
@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    try:
        item_dict = dict(item)
        item_dict["expiry_date"] = datetime.combine(item.expiry_date, datetime.min.time())
        item_dict["insert_date"] = datetime.now()
        new_item = db["Items"].insert_one(item_dict)
        created_item = db["Items"].find_one({"_id": new_item.inserted_id})
        return item_helper(created_item)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Retriving the items using filters
@router.get("/items/filter", status_code=status.HTTP_200_OK)
async def filter_items(
    email: Optional[str] = Query(None, description="Filter by email"),
    expiry_date: Optional[str] = Query(None, description="Filter items expiring after the provided date (YYYY-MM-DD)"),
    insert_date: Optional[str] = Query(None, description="Filter items inserted after the provided date (YYYY-MM-DD)"),
    quantity: Optional[int] = Query(None, description="Filter items with quantity greater than or equal to the provided number"),
    aggregation: Optional[bool] = Query(False, description="Set to true to aggregate data by email")
):
    try:
        query = {}

        if email:
            query["email"] = email

        if expiry_date:
            try:
                expiry_date_dt = datetime.strptime(expiry_date, "%Y-%m-%d")
                query["expiry_date"] = {"$gt": expiry_date_dt}
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid expiry date format. Use YYYY-MM-DD.")
        
        if insert_date:
            try:
                insert_date_dt = datetime.strptime(insert_date, "%Y-%m-%d")
                query["insert_date"] = {"$gt": insert_date_dt}
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid insert date format. Use YYYY-MM-DD.")

        if quantity:
            query["quantity"] = {"$gte": quantity}

        if aggregation:
            pipeline = [
            {"$match": query},
            {"$group": {"_id": "$email", "count": {"$sum": 1}}},
            {"$project": {"email": "$_id", "count": 1, "_id": 0}}  # Properly handle _id field
        ]

            try:
                results = list(db["Items"].aggregate(pipeline))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            results = list(db["Items"].find(query))

        for item in results:
            if item.get("_id"):
                item["_id"] = str(item["_id"])
        
        return results

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Retriving the item using id
@router.get("/items/{id}", status_code=status.HTTP_200_OK)
async def get_item(id: str):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Item ID.")

        item = db["Items"].find_one({"_id": ObjectId(id)})
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")
        return item_helper(item)
    
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Deleting the item using id
@router.delete("/items/{id}", status_code=status.HTTP_200_OK)
async def delete_item(id: str):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Item ID format.")

        result = db["Items"].delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

        return {"message": "Item deleted successfully"}

    except HTTPException as httpexc:
        raise httpexc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Updating the item using id
@router.put("/items/{id}", status_code=status.HTTP_200_OK)
async def update_item(id: str, item: Item):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Item ID.")
        

        item.expiry_date = datetime.combine(item.expiry_date, datetime.min.time())

        update_data = {"name": item.name, "email": item.email, "item_name": item.item_name, "quantity": item.quantity, "expiry_date": item.expiry_date}
        
        if update_data:
            result = db["Items"].update_one({"_id": ObjectId(id)},{"$set": update_data})
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update provided.")

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Item not found.")

        return {"message": "Item updated successfully"}

    except HTTPException as httpexc:
        raise httpexc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
