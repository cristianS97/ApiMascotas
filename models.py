from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Mascota(Base):
    __tablename__ = 'mascota'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    especie = Column(String)
    raza = Column(String)
    edad = Column(Integer)
