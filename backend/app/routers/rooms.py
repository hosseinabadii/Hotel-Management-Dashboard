from fastapi import APIRouter, status

from app.db.main import SessionDep
from app.operations import rooms
from app.operations.schemas import RoomCreateData, RoomPublic, RoomUpdateData

router = APIRouter()


@router.get("/", response_model=list[RoomPublic])
async def read_all_rooms(session: SessionDep):
    return await rooms.read_all_rooms(session)


@router.get("/{room_id}", response_model=RoomPublic)
async def read_room(room_id: int, session: SessionDep):
    return await rooms.read_room(session, room_id)


@router.post("/", response_model=RoomPublic, status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomCreateData, session: SessionDep):
    return await rooms.create_room(session, room)


@router.put("/{room_id}", response_model=RoomPublic, status_code=status.HTTP_202_ACCEPTED)
async def update_room(room_id: int, room: RoomUpdateData, session: SessionDep):
    return await rooms.update_room(session, room_id, room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, session: SessionDep):
    return await rooms.delete_room(session, room_id)
