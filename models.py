from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Raza(Base):
    __tablename__ = 'raza'
    id = Column(Integer, primary_key=True)
    especie = Column(String)
    raza = Column(String)
    mascotas = relationship("Mascota", back_populates="raza_obj")

class Mascota(Base):
    __tablename__ = 'mascota'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    edad = Column(Integer)
    raza_id = Column(Integer, ForeignKey('raza.id'))
    raza_obj = relationship("Raza", back_populates="mascotas")
