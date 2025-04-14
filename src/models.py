import datetime
import enum
from typing import Annotated, Optional,Any

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    text,LargeBinary)
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from geoalchemy2 import Geometry
from .database import Base, str_256

    

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]



class ClientsOrm(Base):
    __tablename__= "clients"
     
    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[Optional[str]]=mapped_column(String(20))
    client_avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    phone_number: Mapped[str] = mapped_column(String(20)) 
    orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="client",)
    jewelers_for_client: Mapped[list["JewelersOrm"]] = relationship(
        back_populates="clients_for_jeweler",
        secondary="m2m_jewelers_clients",
    )
   

class Workload(enum.Enum):
    repair = "ремонт"
    production = "изготовление"
    both_add = "ремонт и изготовление"


class JewelersOrm(Base):
    __tablename__ = "jewelers"
     

    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[Optional[str]]=mapped_column(String(30))
    workload:Mapped[Workload]
    # jeweler_avatar: Mapped [Optional[bytes]] = mapped_column(LargeBinary)
    phone_number: Mapped[str] = mapped_column(String(30))
    adress: Mapped[str] = mapped_column(String(256)) 
    orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="jeweler",
    )
    clients_for_jeweler: Mapped[list["ClientsOrm"]] = relationship(
        back_populates="jewelers_for_client",
        secondary="m2m_jewelers_clients",
    )
   
    
# class Geometry_Order(Geometry):
#     geometry_type: str | None = "GEOMETRY",
#     srid: int = -1,
#     dimension: int = 2,
#     spatial_index: bool = True,
#     use_N_D_index: bool = False,
#     use_typmod: bool | None = None,
#     from_text: str | None = None,
#     name: str | None = None,
#     nullable: bool = True,
#     _spatial_index_reflected: Any | None = None

class M2mJewelersClientsORM(Base):
    __tablename__ = "m2m_jewelers_clients"

    jeweler_id: Mapped[int]=mapped_column(ForeignKey("jewelers.id", ondelete="CASCADE"),
        primary_key=True,
    )
    client_id: Mapped[int]=mapped_column(ForeignKey("clients.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cover_letter: Mapped[Optional[str]]



    


class OrdersOrm(Base):
    __tablename__ = "orders"

    id: Mapped[intpk]
    title: Mapped[str_256]
    image_order_path: Mapped[Optional[str]] = mapped_column(String(255))
    workload: Mapped[Workload]
    compensation: Mapped[Optional[int]]
    jeweler_id: Mapped[Optional[int]] = mapped_column(ForeignKey("jewelers.id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id",ondelete="CASCADE"))
    # Геометрия точки (долгота, широта)
    # location: Mapped[str | None] = mapped_column(Geometry_Order('POINT'), nullable=True)
    jeweler: Mapped[Optional["JewelersOrm"]] = relationship(
        back_populates="orders",)
    client: Mapped["ClientsOrm"] = relationship(
        back_populates="orders",)





