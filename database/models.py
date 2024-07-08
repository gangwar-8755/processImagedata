from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    products = relationship("Product", back_populates="request")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    serial_number = Column(Integer, nullable=False)
    product_name = Column(String(255), nullable=False)
    input_image_urls = Column(Text, nullable=False)
    output_image_urls = Column(Text, nullable=True)
    request = relationship("Request", back_populates="products")
