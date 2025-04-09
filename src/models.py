import datetime
import enum
from typing import Annotated, Optional

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

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]



class JewelersOrm(Base):
    __tablename__ = "jewelers"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[intpk]
    username: Mapped[str]
    jeweler_avatar: Mapped[bytes | None] = mapped_column(LargeBinary)
    phone_number: Mapped[str] = mapped_column(String(20)) 
    orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="jeweler",
    )

    resumes_parttime: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="jeweler",
        primaryjoin="and_(JewelersOrm.id == OrdersOrm.jeweler_id, OrdersOrm.workload == 'parttime')",
        order_by="OrdersOrm.id.desc()",
    )
    

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class OrdersOrm(Base):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[intpk]
    title: Mapped[str_256]
    image_order_path: Mapped[str | None] = mapped_column(String(255))
    workload: Mapped[Workload]
    jeweler_id: Mapped[int] = mapped_column(ForeignKey("jewelers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id",ondelete="CASCADE"))

    jeweler: Mapped["JewelersOrm"] = relationship(
        back_populates="orders",
    )
    client: Mapped["ClientsOrm"] = relationship(
        back_populates="orders",)


class ClientsOrm(Base):
    __tablename__= "clients"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[intpk]
    username: Mapped[str]
    client_avatar: Mapped[bytes | None] = mapped_column(LargeBinary)
    phone_number: Mapped[str] = mapped_column(String(20)) 
    clients_orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="client",)
    orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="client")


