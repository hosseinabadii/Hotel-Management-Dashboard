from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DBCustomer
from app.operations.schemas import CustomerCreateData, CustomerUpdateData


async def read_all_customers(session: AsyncSession) -> Sequence[DBCustomer]:
    statement = select(DBCustomer)
    result = await session.execute(statement)
    return result.scalars().all()


async def read_customer(session: AsyncSession, customer_id: int) -> DBCustomer:
    db_customer = await session.get(DBCustomer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


async def create_customer(session: AsyncSession, data: CustomerCreateData):
    db_customer = DBCustomer(**data.model_dump())
    session.add(db_customer)
    await session.commit()
    return db_customer


async def update_customer(session: AsyncSession, customer_id: int, data: CustomerUpdateData) -> DBCustomer:
    db_customer = await read_customer(session, customer_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    await session.commit()
    await session.refresh(db_customer)
    return db_customer


async def delete_customer(session: AsyncSession, customer_id: int) -> None:
    db_customer = await read_customer(session, customer_id)
    await session.delete(db_customer)
    await session.commit()
