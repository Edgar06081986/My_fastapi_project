from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr
from typing import Optional
from datetime import datetime
from src.models.models import Workload
from src.clients.cli_schemas import ClientsDTO
from src.jewelers.jew_schemas import JewelersDTO


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
