from datetime import datetime
from typing import Optional
import re
from pydantic import BaseModel, ConfigDict,Field,EmailStr,field_validator,HttpUrl


from src.models import Workload


class JewelersAddDTO(BaseModel):
    jeweler_avatar_url: Optional[HttpUrl] = None  # Автоматическая валидация URL
    username: str = Field(min_length=1, max_length=60)
    workload: Workload
    phone_number: str = Field(min_length=5, max_length=15)
    address: str = Field(min_length=1, max_length=256)
    email: EmailStr | None
    
    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(r"^\+?[\d\s\-\(\)]{5,15}$", v):
            raise ValueError("Invalid phone number format")
        return v
    
    model_config = ConfigDict(
    extra="forbid",
    json_schema_extra={
        "examples": [{
            "username": "johndoe",
            "workload": "medium",
            "phone_number": "+71234567890",
            "address": "город Краснодар,улица Красная,дом 5 ",
            "email": "john@example.com"
        }]
    }
)
   
      

class JewelersDTO(JewelersAddDTO):
    id: int 


class ClientsAddDTO(BaseModel):
    username: str = Field(min_length=1, max_length=35)
    client_avatar_url: Optional[HttpUrl] = None  # Автоматическая валидация URL
    phone_number: str = Field(min_length=5, max_length=20) 
    email:EmailStr|None
    model_config = ConfigDict(
    extra="forbid",
    json_schema_extra={
        "examples": [{
            "username": "john_doe",
            "phone_number": "+1234567890",
            "email": "john@example.com"
        }]
    }
)

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(r"^\+?[\d\s\-\(\)]{5,20}$", v):
            raise ValueError("Invalid phone number format")
        return v
    
    # @field_validator("client_avatar_url")
    # def validate_image_path(cls, v):
    #     if v and not v.endswith((".jpg", ".png")):
    #         raise ValueError("Only .jpg or .png allowed")
    #     return v

class ClientsDTO(ClientsAddDTO):
    id: int
  

class OrdersAddDTO(BaseModel):
    title: str = Field(max_length=360)
    compensation: Optional[int] = Field(None, ge=0)  # ≥ 0 или None
    workload: Workload  # Только значения из Enum
    order_avatar_url: Optional[HttpUrl] = None  # Автоматическая валидация URL
    jeweler_id: Optional[int] = Field(None, ge=1)  # ≥ 1 или None
    client_id: int = Field(ge=0, le=130)  # 0 ≤ client_id ≤ 130

    # @field_validator("order_foto_url")
    # def validate_image_path(cls, v):
    #     if v and not v.endswith((".jpg", ".png")):
    #         raise ValueError("Only .jpg or .png allowed")
    #     return v



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