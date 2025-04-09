from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from models import Workload


class JewelersAddDTO(BaseModel):
    username: str

class JewelersDTO(JewelersAddDTO):
    id: int

class ClientsAddDTO(BaseModel):
    username: str

class ClientsDTO(ClientsAddDTO):
    id: int



class OrdersAddDTO(BaseModel):
    title: str
    compensation: Optional[int]
    workload: Workload
    worker_id: int
    client_id; int

class OrdersDTO(OrdersAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class OrdersRelDTO(OrdersDTO):
    jeweler: "JewelersDTO"
    client: "ClientsDTO"

class JewelersRelDTO(JewelersDTO):
    orders: list["OrdersDTO"]


class ClientsRelDTO(ClientsDTO):
    client_orders: list["OrdersDTO"]