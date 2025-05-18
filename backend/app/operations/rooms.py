from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DBRoom
from app.operations.schemas import RoomCreateData, RoomUpdateData


async def read_all_rooms(session: AsyncSession) -> Sequence[DBRoom]:
    statement = select(DBRoom)
    result = await session.execute(statement)
    return result.scalars().all()


async def read_room(session: AsyncSession, room_id: int) -> DBRoom:
    db_room = await session.get(DBRoom, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


async def create_room(session: AsyncSession, data: RoomCreateData) -> DBRoom:
    db_room = DBRoom(**data.model_dump())
    session.add(db_room)
    await session.commit()
    return db_room


async def update_room(session: AsyncSession, room_id: int, data: RoomUpdateData) -> DBRoom:
    db_room = await read_room(session, room_id)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    await session.commit()
    await session.refresh(db_room)
    return db_room


async def delete_room(session: AsyncSession, room_id: int) -> None:
    db_room = await read_room(session, room_id)
    await session.delete(db_room)
    await session.commit()
