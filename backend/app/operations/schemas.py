from datetime import date, timedelta

from pydantic import BaseModel, ConfigDict


# Customers schemas
class CustomerCreateData(BaseModel):
    first_name: str
    last_name: str
    email_address: str


class CustomerUpdateData(BaseModel):
    first_name: str | None
    last_name: str | None
    email_address: str | None


class CustomerPublic(BaseModel):
    id: int
    first_name: str
    last_name: str
    email_address: str

    model_config = ConfigDict(from_attributes=True)


# Rooms schemas
class RoomCreateData(BaseModel):
    number: str
    size: int
    price: int


class RoomUpdateData(BaseModel):
    number: str | None
    size: int | None
    price: int | None


class RoomPublic(BaseModel):
    id: int
    number: str
    size: int
    price: int

    model_config = ConfigDict(from_attributes=True)


# Booking schemas
class BookingCreateData(BaseModel):
    room_id: int
    customer_id: int
    from_date: date = date.today()
    to_date: date = date.today() + timedelta(days=2)


class BookingUpdateData(BaseModel):
    room_id: int | None
    customer_id: int | None
    from_date: date | None
    to_date: date | None


class BookingPublic(BaseModel):
    id: int
    room_id: int
    customer_id: int
    price: int
    from_date: date
    to_date: date

    model_config = ConfigDict(from_attributes=True)
