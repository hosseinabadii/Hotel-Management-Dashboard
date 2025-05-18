from collections.abc import Sequence
from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import DBBooking
from app.operations.customers import read_customer
from app.operations.rooms import read_room
from app.operations.schemas import BookingCreateData, BookingUpdateData


def date_validation(from_date: date, to_date: date) -> int:
    days = (to_date - from_date).days
    if days <= 0:
        raise HTTPException(status_code=422, detail="Invalid dates")
    return days


async def read_all_bookings(session: AsyncSession) -> Sequence[DBBooking]:
    statement = select(DBBooking)
    result = await session.execute(statement)
    return result.scalars().all()


async def read_booking(session: AsyncSession, booking_id: int) -> DBBooking:
    db_booking = await session.get(DBBooking, booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


async def read_booking_with_details(session: AsyncSession, booking_id: int) -> DBBooking:
    statement = (
        select(DBBooking)
        .where(DBBooking.id == booking_id)
        .options(joinedload(DBBooking.customer), joinedload(DBBooking.room))
    )
    result = await session.execute(statement)
    db_booking = result.unique().scalar_one_or_none()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


async def create_booking(session: AsyncSession, data: BookingCreateData) -> DBBooking:
    await read_customer(session, data.customer_id)
    room = await read_room(session, data.room_id)
    days = date_validation(data.from_date, data.to_date)
    price = room.price * days
    db_booking = DBBooking(**data.model_dump(), price=price)
    session.add(db_booking)
    await session.commit()
    return db_booking


async def update_booking(session: AsyncSession, booking_id: int, data: BookingUpdateData) -> DBBooking:
    db_booking = await read_booking_with_details(session, booking_id)
    room = db_booking.room
    if (data.room_id is not None) and (data.room_id != db_booking.room_id):
        room = await read_room(session, data.room_id)

    if (data.customer_id is not None) and (data.customer_id != db_booking.customer_id):
        await read_customer(session, data.customer_id)

    from_date = data.from_date
    if from_date is None:
        from_date = db_booking.from_date

    to_date = data.to_date
    if to_date is None:
        to_date = db_booking.to_date

    days = date_validation(from_date, to_date)
    price = room.price * days
    update_data = data.model_dump(exclude_unset=True)
    update_data.update(price=price)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    await session.commit()
    await session.refresh(db_booking)
    return db_booking


async def delete_booking(session: AsyncSession, booking_id: int) -> None:
    db_booking = await read_booking(session, booking_id)
    await session.delete(db_booking)
    await session.commit()
