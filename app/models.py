from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")



class RestaurantTable(Base):

    __tablename__ = "restaurant_tables"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

    #связь с бронированиями
    bookings: Mapped[list["Booking"]] = relationship("Booking",
    back_populates="table", cascade="all, delete-orphan")

class Booking(Base):

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    table_id: Mapped[int] = mapped_column(ForeignKey("restaurant_tables.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    guest_name: Mapped[str] = mapped_column(String(100), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    #связь со столом
    table: Mapped["RestaurantTable"] = relationship("RestaurantTable", 
    back_populates="bookings")

    user: Mapped["User"] = relationship("User", back_populates="bookings")

