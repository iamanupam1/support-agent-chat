from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    status = Column(String)
    total_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey('orders.order_id'))
    product_id = Column(String, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class SupportTicket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    order_id = Column(String, ForeignKey('orders.order_id'))
    issue = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    order = relationship("Order")
