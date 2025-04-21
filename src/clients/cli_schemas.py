from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional
import re
from src.orders.ord_schemas import OrdersDTO


class ClientsAddDTO(BaseModel):
    username: str = Field(min_length=1, max_length=35)
    client_avatar_url: Optional[str] = None  # Автоматическая валидация URL
    phone_number: str = Field(min_length=5, max_length=20)
    email: EmailStr | None
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

    # @field_validator("phone_number")
    # def validate_phone_number(cls, v):
    #     if not re.match(r"^\+?[\d\s\-\(\)]{5,20}$", v):
    #         raise ValueError("Invalid phone number format")
    #     return v

    # @field_validator("client_avatar_url")
    # def validate_image_path(cls, v):
    #     if v and not v.endswith((".jpg", ".png")):
    #         raise ValueError("Only .jpg or .png allowed")
    #     return v


class ClientsDTO(ClientsAddDTO):
    id: int


class ClientsRelDTO(ClientsDTO):
    orders: list["OrdersDTO"]
