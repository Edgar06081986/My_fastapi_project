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
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]


a=34

class JewelersOrm(Base):
    __tablename__ = "jewelers"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[intpk]
    username: Mapped[str]

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
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("jewelers.id", ondelete="CASCADE"))
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
    clients_orders: Mapped[list["OrdersOrm"]] = relationship(
        back_populates="client",)


    # vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
    #     back_populates="resumes_replied",
    #     secondary="vacancies_replies",
    # )

    # repr_cols_num = 2
    # repr_cols = ("created_at", )

    # __table_args__ = (
    #     Index("title_index", "title"),
    #     CheckConstraint("compensation > 0", name="checl_compensation_positive"),
    # )


# class VacanciesOrm(Base):
#     __tablename__ = "vacancies"

#     id: Mapped[intpk]
#     title: Mapped[str_256]
#     compensation: Mapped[Optional[int]]

#     resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
#         back_populates="vacancies_replied",
#         secondary="vacancies_replies",
#     )


# class VacanciesRepliesOrm(Base):
#     __tablename__ = "vacancies_replies"

#     resume_id: Mapped[int] = mapped_column(
#         ForeignKey("resumes.id", ondelete="CASCADE"),
#         primary_key=True,
#     )
#     vacancy_id: Mapped[int] = mapped_column(
#         ForeignKey("vacancies.id", ondelete="CASCADE"),
#         primary_key=True,
#     )

#     cover_letter: Mapped[Optional[str]]
