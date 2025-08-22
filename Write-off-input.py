# backend/main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId
import shutil
from datetime import datetime

# MongoDB 連線
client = MongoClient("mongodb://localhost:27017/")
db = client["office_system"]
collection = db["finance_records"]

# Pydantic model
class FinanceRecord(BaseModel):
    project_name: str
    category: str
    amount: float
    payment_method: str
    remark: str | None = None

# 建立核銷紀錄
@app.post("/finance/records")
async def create_record(
    project_name: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    payment_method: str = Form(...),
    remark: str = Form(""),
    receipt: UploadFile | None = None
):
    file_path = None
    if receipt:
        file_path = f"uploads/{receipt.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(receipt.file, buffer)

    record = {
        "project_name": project_name,
        "category": category,
        "amount": amount,
        "payment_method": payment_method,
        "receipt_file": file_path,
        "remark": remark,
        "created_at": datetime.utcnow().isoformat()
    }

    result = collection.insert_one(record)
    return {"message": "Record created", "id": str(result.inserted_id)}

# 查詢所有核銷紀錄
@app.get("/finance/records")
async def get_records():
    records = []
    for r in collection.find().sort("created_at", -1):
        records.append({
            "id": str(r["_id"]),
            "project_name": r["project_name"],
            "category": r["category"],
            "amount": r["amount"],
            "payment_method": r["payment_method"],
            "receipt_file": r.get("receipt_file"),
            "remark": r.get("remark"),
            "created_at": r["created_at"],
        })
    return records
