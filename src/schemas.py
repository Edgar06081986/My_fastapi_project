from datetime import datetime
from typing import Optional
import re
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


from src.models import Workload


class JewelersRelDTO(JewelersDTO):
    orders: list["OrdersDTO"]
