from fastapi import APIRouter, status, HTTPException, Query
from app.models import ClockIn
from app.config import db
from app.utils import clock_in_helper, is_valid_objectid
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

router  = APIRouter()


@router.post("/clock-in", status_code=status.HTTP_201_CREATED)
async def create_clock_in_record(clock_in: ClockIn):
    try:
        clock_in_dict = dict(clock_in)
        clock_in_dict["insert_date"] = datetime.now()
        
        new_record = db["ClockInRecords"].insert_one(clock_in_dict)
        created_record = db["ClockInRecords"].find_one({"_id": new_record.inserted_id})
        return clock_in_helper(created_record)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/clock-in/filter", response_model=List[dict], status_code=status.HTTP_200_OK)
async def filter_clock_in_records(
    email: Optional[str] = Query(None, description="Filter by email"),
    location: Optional[str] = Query(None, description="Filter by location"),
    insert_date: Optional[str] = Query(None, description="Filter clock-ins after the provided date (YYYY-MM-DD)")
):
    try:
        query = {}
        if email:
            query["email"] = email

        if location:
            query["location"] = location

        if insert_date:
            try:
                insert_date_dt = datetime.strptime(insert_date, "%Y-%m-%d")
                query["insert_date"] = {"$gt": insert_date_dt}
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid insert_datetime format. Use YYYY-MM-DD.")

        clock_in_records = list(db["ClockInRecords"].find(query))

        for c in clock_in_records:
            c["_id"] = str(c["_id"])
        
        return clock_in_records
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/clock-in/{id}", status_code=status.HTTP_200_OK)
async def get_clock_in_record(id: str):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Clock-in ID.")
        
        record = db["ClockInRecords"].find_one({"_id": ObjectId(id)})
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock-in-Record not found.")

        return clock_in_helper(record)
    
    except HTTPException as httpexc:
        raise httpexc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/clock-in/{id}", status_code=status.HTTP_200_OK)
async def delete_clock__in_record(id: str):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Clock in Record ID.")

        result = db["ClockInRecords"].delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock in Record not found.")
        
        return {"message" : "Clock in Record deleted successfully"}

    except HTTPException as httpexc:
        raise httpexc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 


@router.put("/clock-in/{id}", status_code=status.HTTP_200_OK)
async def update_clock_in_record(id: str, update_data: ClockIn):
    try:
        if not is_valid_objectid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Clock in Record ID.")
        
        update_fields = {"email": update_data.email, "location": update_data.location}
        result = db["ClockInRecords"].update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clock in Record not found.")
        
        return {"message": "Clock in Record updated successfully"}

    except HTTPException as httpexc:
        raise httpexc
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))