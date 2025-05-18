from fastapi import APIRouter, status

from app.db.main import SessionDep
from app.operations import customers
from app.operations.schemas import CustomerCreateData, CustomerPublic, CustomerUpdateData

router = APIRouter()


@router.get("/", response_model=list[CustomerPublic])
async def read_all_customers(session: SessionDep):
    return await customers.read_all_customers(session)


@router.get("/{customer_id}", response_model=CustomerPublic)
async def read_customer(customer_id: int, session: SessionDep):
    return await customers.read_customer(session, customer_id)


@router.post("/", response_model=CustomerPublic, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreateData, session: SessionDep):
    return await customers.create_customer(session, customer)


@router.put("/{customer_id}", response_model=CustomerPublic, status_code=status.HTTP_202_ACCEPTED)
async def update_customer(customer_id: int, customer: CustomerUpdateData, session: SessionDep):
    return await customers.update_customer(session, customer_id, customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session: SessionDep):
    return await customers.delete_customer(session, customer_id)
