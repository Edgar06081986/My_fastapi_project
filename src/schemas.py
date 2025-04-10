from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict,fields,Field,EmailStr

from models import Workload


class JewelersAddDTO(BaseModel):
    username: str
    workload:Workload
    jeweler_avatar: Optional[bytes]
    phone_number:str = Field(max_length= 15)
    adress:str
    email: EmailStr

class JewelersDTO(JewelersAddDTO):
    id: int =  Field(ge=0, le=130)


class ClientsAddDTO(BaseModel):
    username: str
    client_avatar: Optional[bytes]
    phone_number:str = Field(max_length= 15)
    email: EmailStr



class ClientsDTO(ClientsAddDTO):
    id: int = Field(ge=0, le=130)



class OrdersAddDTO(BaseModel):
    title: str
    compensation: Optional[int]= Field(ge=0, le=130)
    workload: Workload
    worker_id: int= fields.Field(..., description="")
    client_id: int= fields.Field(..., description="")
    title:str= fields.Field(..., description="")
    image_order_path:Optional[str]
    workload: Workload
    compensation: Optional[int] = Field(ge=0, le=130)
    jeweler_id: Optional[int]=Field(ge=0, le=130)
    client_id:int = fields.Field(..., description="")



class OrdersDTO(OrdersAddDTO):
    id: int = Field(ge=0, le=130)
    created_at: datetime
    updated_at: datetime

class OrdersRelDTO(OrdersDTO):
    jeweler: Optional["JewelersDTO"]
    client: "ClientsDTO"

class JewelersRelDTO(JewelersDTO):
    orders: list["OrdersDTO"]


class ClientsRelDTO(ClientsDTO):
    orders: list["OrdersDTO"]