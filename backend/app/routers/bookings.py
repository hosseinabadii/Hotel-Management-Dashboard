from fastapi import APIRouter, status

from app.db.main import SessionDep
from app.operations import bookings
from app.operations.schemas import BookingCreateData, BookingPublic, BookingUpdateData

router = APIRouter()


@router.get("/", response_model=list[BookingPublic])
async def read_all_bookings(session: SessionDep):
    return await bookings.read_all_bookings(session)


@router.get("/{booking_id}", response_model=BookingPublic)
async def read_booking(booking_id: int, session: SessionDep):
    return await bookings.read_booking(session, booking_id)


@router.post("/", response_model=BookingPublic, status_code=status.HTTP_201_CREATED)
async def create_booking(booking: BookingCreateData, session: SessionDep):
    return await bookings.create_booking(session, booking)


@router.put("/{booking_id}", response_model=BookingPublic, status_code=status.HTTP_202_ACCEPTED)
async def update_booking(booking_id: int, booking: BookingUpdateData, session: SessionDep):
    return await bookings.update_booking(session, booking_id, booking)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, session: SessionDep):
    return await bookings.delete_booking(session, booking_id)
