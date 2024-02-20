from typing import List
from sqlalchemy import ForeignKey, TIMESTAMP, Integer, Float, String, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    orders: Mapped[List["Order"]] = relationship()


class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[int] = mapped_column(TIMESTAMP)
    total_price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    items: Mapped[List["OrderItem"]] = relationship()
    follow_up: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    user: Mapped["User"] = relationship(back_populates='orders')


class OrderItem(Base):
    __tablename__ = "order_item"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    count: Mapped[int] = mapped_column(Integer)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship()


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)


