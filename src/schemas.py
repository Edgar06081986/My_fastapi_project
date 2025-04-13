from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict,fields,Field,EmailStr

from .models import Workload


class JewelersAddDTO(BaseModel):
    username: str
    workload:Workload
    jeweler_avatar: Optional[bytes]
    phone_number:str = Field(max_length= 15)
    adress: str = Field(max_length= 256)
    email: str = Field(EmailStr)
    model_config = ConfigDict()
class JewelersDTO(JewelersAddDTO):
    id: int 
  


class ClientsAddDTO(BaseModel):
    username: str
    client_avatar: Optional[bytes]
    phone_number:str = Field(max_length= 15)
    email: str= Field(EmailStr)



class ClientsDTO(ClientsAddDTO):
    id: int
  


class OrdersAddDTO(BaseModel):
    title: str= Field( max_length=360)
    compensation: Optional[int]
    workload: Workload 
    image_order_path:Optional[str]
    jeweler_id: Optional[int]
    client_id:int = fields.Field(ge=0, le=130)



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