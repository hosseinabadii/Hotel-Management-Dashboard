import asyncio
import random
from datetime import date, timedelta

from .main import async_session, init_db
from .models import DBBooking, DBCustomer, DBRoom

customers = [
    DBCustomer(first_name="John", last_name="Smith", email_address="email@email.com"),
    DBCustomer(first_name="Jane", last_name="Doe", email_address="jane@hotmail.com"),
    DBCustomer(first_name="Jack", last_name="Black", email_address="jack@black.com"),
    DBCustomer(first_name="Jill", last_name="White", email_address="jill@gmail.com"),
]

rooms = [
    DBRoom(number="101", size=10, price=150_00),
    DBRoom(number="102", size=10, price=150_00),
    DBRoom(number="103", size=20, price=250_00),
    DBRoom(number="104", size=20, price=250_00),
    DBRoom(number="105", size=30, price=350_00),
]


def generate_random_booking(customer_ids, room_ids):
    today = date.today()
    start_date = today + timedelta(days=random.randint(1, 180))
    end_date = start_date + timedelta(days=random.randint(1, 14))

    customer_id = random.choice(customer_ids)
    room_id = random.choice(room_ids)

    room = next(r for r in rooms if r.id == room_id)

    nights = (end_date - start_date).days
    total_price = room.price * nights

    return DBBooking(
        from_date=start_date,
        to_date=end_date,
        price=total_price,
        customer_id=customer_id,
        room_id=room_id,
    )


async def main():
    await init_db()
    print("Populating database...")
    async with async_session() as session:
        session.add_all(customers)
        session.add_all(rooms)
        await session.commit()

        await session.refresh(customers[0])
        await session.refresh(rooms[0])

        customer_ids = [customer.id for customer in customers]
        room_ids = [room.id for room in rooms]

        bookings = [generate_random_booking(customer_ids, room_ids) for _ in range(10)]
        session.add_all(bookings)

        await session.commit()
        print("Successfully Done!")


if __name__ == "__main__":
    asyncio.run(main())
