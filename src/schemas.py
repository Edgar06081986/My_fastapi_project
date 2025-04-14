from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict,Field,EmailStr,ByteSize


from src.models import Workload


class JewelersAddDTO(BaseModel):
    username: str=Field(max_length=60)
    workload:Workload 
    # jeweler_avatar:bytes | None
    phone_number:str = Field(max_length= 15)
    adress: str = Field(max_length= 256)
    email: EmailStr|None
    model_config=ConfigDict(extra="forbid")

class JewelersDTO(JewelersAddDTO):
    id: int 


class ClientsAddDTO(BaseModel):
    username: str=Field(max_length=35)
    phone_number:str = Field(max_length= 20)
    email:EmailStr|None
    model_config=ConfigDict(extra="forbid")


class ClientsDTO(ClientsAddDTO):
    id: int
  


class OrdersAddDTO(BaseModel):
    title: str = Field( max_length=360)
    compensation: Optional[int]
    workload: str = Workload 
    image_order_path:Optional[str]
    jeweler_id: Optional[int]
    client_id:int = Field(ge=0, le=130)
    model_config=ConfigDict(extra="forbid")


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