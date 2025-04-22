from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional
import re
from src.models.models import Workload


class JewelersAddDTO(BaseModel):
    jeweler_avatar_url: Optional[str] = None  # Автоматическая валидация URL
    username: str = Field(min_length=1, max_length=60)
    workload: Workload
    phone_number: str = Field(min_length=5, max_length=15)
    address: str = Field(min_length=1, max_length=256)
    email: str = EmailStr | None
    portfolio: Optional[str] = None

    @field_validator("jeweler_avatar_url")
    def validate_url(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("URL должен начинаться с http:// или https://")
        return v

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not re.match(r"^\+?[\d\s\-\(\)]{5,20}$", v):
            raise ValueError("Invalid phone number format")
        return v

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "examples": [
                {
                    "username": "johndoe",
                    "workload": "medium",
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


class JewelersRelDTO(JewelersDTO):
    orders: list["OrdersDTO"]
