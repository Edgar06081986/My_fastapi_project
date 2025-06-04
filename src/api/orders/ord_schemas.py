from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime
from src.models.models import Workload
from src.api.jewelers.jew_schemas import JewelersDTO


class OrdersAddDTO(BaseModel):
    title: str = Field(max_length=360)
    compensation: Optional[int] = Field(None, ge=0)  # ≥ 0 или None
    workload: Workload  # Только значения из Enum
    order_avatar_url: Optional[str] = None  # Автоматическая валидация URL
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


class ClientsAddDTO(BaseModel):
    username: str = Field(min_length=1, max_length=35)
    client_avatar_url: Optional[str] = None  # Автоматическая валидация URL
    phone_number: str = Field(min_length=5, max_length=20)
    email: Optional[EmailStr] = Field(default=None, json_schema_extra={"default": None})
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "username": "john_doe",
                    "phone_number": "+1234567890",
                    "email": "john@example.com",
                }
            ]
        },
    )


class ClientsDTO(ClientsAddDTO):
    id: int
