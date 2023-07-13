from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class User():
    __tablename__ = "region"

    region_id = Column(Integer, primary_key=True, index=True)
    region_description = Column(String, unique=True, index=True)
