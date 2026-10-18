from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.redis_client import redis_client

from app.database import get_db
from app.models import RestaurantTable
from app.schemas import TableCreate, TableResponse
from app.security import get_current_user

router = APIRouter(prefix="/tables", tags=["столы"])

@router.post("",
response_model=TableResponse,
status_code=status.HTTP_201_CREATED)
async def create_table(data: TableCreate, db: AsyncSession = Depends(get_current_user)):
    result = await db.execute(select(RestaurantTable).where(RestaurantTable.number == data.number))
    if result.scalar_one_or_none() is not None:
        raise 
    HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"стол с номером {data.number}"
        )
    table = RestaurantTable(number=data.number,
                            capacity=data.capacity)
    db.add(table)
    await db.commit()
    await db.refresh(table)
    await redis_client.delete("all_tables")
    return table

@router.get("",
response_model=list[TableResponse])
async def get_tables(db: AsyncSession = Depends(get_db)):
    cached = await redis_client.get("all_tables")
    if cached:
        return json.loads(cached)

    result = await db.execute(select(RestaurantTable).order_by(RestaurantTable.number))
    tables = result.scalars().all()

    tables_json = json.dumps([TableResponse.model_validate(t).model_dump()
                              for t in tables])
    await redis_client.set("all_tables", tables_json, ex=60)
    return tables
