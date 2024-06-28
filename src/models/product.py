from sqlalchemy import Column, String, Text, JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    pricing = Column(JSON)
    availability = Column(JSON)
    category = Column(String)
