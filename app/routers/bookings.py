from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Booking, RestaurantTable, User
from app.schemas import BookingCreate, BookingResponse
from app.security import get_current_user
from app.services.telegram_bot import send_telegram_notification

router = APIRouter(prefix="/bookings", tags=[",reservation"])

@router.post("",
response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    result = await db.execute(
        select(RestaurantTable).where(RestaurantTable.id ==
        data.table_id).with_for_update()
    )
    table = result.scalar_one_or_none()
    if not table:
        raise 
    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="table not found")
    existing = await db.execute(
        select(Booking).where(
            Booking.table_id == data.table_id,
            Booking.starts_at == data.starts_at
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise 
    HTTPException(status_code=status.HTTP_409_CONFLICT, detail="this time slot is aready booking")
    booking = Booking(
        table_id=data.table_id,
        user_id=current_user.id,
        guest_name=data.guest_name,
        starts_at=data.starts_at
    )
    db.add(booking)
    await  db.commit()
    await db.refresh(booking)

    await send_telegram_notification(
        table_number=table.number,
        guest_name=booking.guest_name,
    starts_at=booking.starts_at.strftime("%Y-%m-%d %H:%M")
    )
    return booking

@router.get("",
response_model=list[BookingResponse])
async def get_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    result = await db.execute(select(Booking).order_by(Booking.starts_at))
    return result.scalars().all()

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
async def cancel_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="бронирование не найдено")
    await db.delete(booking)
    await db.commit()
    return {"message": f"бронирование {booking_id} отменено"}

