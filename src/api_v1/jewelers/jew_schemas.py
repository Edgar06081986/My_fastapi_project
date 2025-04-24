from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional
import re
from src.models.models import Workload
from datetime import datetime


class JewelersAddDTO(BaseModel):
    jeweler_avatar_url: Optional[str] = None  # Автоматическая валидация URL
    username: str = Field(min_length=1, max_length=60)
    workload: Workload
    phone_number: str = Field(min_length=5, max_length=30)
    address: str = Field(min_length=1, max_length=256)
    email: Optional[EmailStr] = Field(default=None, json_schema_extra={"default": None})
    portfolio: Optional[str] = None

    @field_validator("jeweler_avatar_url")
    def validate_url(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(r"^\+?[\d\s\-\(\)]{5,30}$", v):
            raise ValueError("Invalid phone number format")
        return v

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "workload": ("repair" or "production" or "production_and_repair"),
                    "phone_number": "+71234567890",
                    "address": "город Краснодар,улица Красная,дом 5 ",
                    "email": "john@example.com",
                }
            ]
        },
    )


class UpdateJewelersDTO(JewelersAddDTO):
    pass


class JewelersDTO(JewelersAddDTO):
    id: int


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


class JewelersRelDTO(JewelersDTO):
    orders: list["OrdersDTO"]
