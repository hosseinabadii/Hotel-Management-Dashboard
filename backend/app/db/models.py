from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DBCustomer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250))
    last_name: Mapped[str] = mapped_column(String(250))
    email_address: Mapped[str] = mapped_column(String(250))


class DBRoom(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(250))
    size: Mapped[int]
    price: Mapped[int]


class DBBooking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_date: Mapped[date]
    to_date: Mapped[date]
    price: Mapped[int] = mapped_column(default=0)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    customer: Mapped[DBCustomer] = relationship()
    room: Mapped[DBRoom] = relationship()
