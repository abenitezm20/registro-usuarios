import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Enum, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from .model import Model
from .db import Base
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields

class TipoIdentificacionEnum(str, enum.Enum):
    tarjeta_identidad = "tarjeta_identidad"
    cedula_ciudadania = "cedula_ciudadania"
    cedula_extranjeria = "cedula_extranjeria"
    pasaporte = "pasaporte"
    registro_civil = "registro_civil"


class GeneroEnum(str, enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"


class Deportista(Model, Base):
    __tablename__ = "deportista"
    nombre = Column(String(50))
    apellido = Column(String(50))
    tipo_identificacion = Column(Enum(TipoIdentificacionEnum))
    numero_identificacion = Column(BigInteger)
    email = Column(String(50), unique=True)
    genero = Column(Enum(GeneroEnum))
    edad = Column(Integer)
    peso = Column(Float)
    altura = Column(Float)
    pais_nacimiento = Column(String(50))
    ciudad_nacimiento = Column(String(50))
    pais_residencia = Column(String(50))
    ciudad_residencia = Column(String(50))
    antiguedad_residencia = Column(Integer)
    contrasena = Column(String(50))
    id_plan_subscripcion = Column(UUID, ForeignKey('plan_subscripcion.id'))
    plan_subscripcion = relationship('PlanSubscripcion')

    def __init__(self, **info_deportista):
        Model.__init__(self)
        self.__dict__.update(info_deportista)


class DeportistaSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    apellido = fields.Str()
    tipo_identificacion = fields.Enum(TipoIdentificacionEnum)
    numero_identificacion = fields.Int()
    email = fields.Str()
    genero = fields.Enum(GeneroEnum)
    edad = fields.Int()
    peso = fields.Float()
    altura = fields.Float()
    pais_nacimiento = fields.Str()
    ciudad_nacimiento = fields.Str()
    pais_residencia = fields.Str()
    ciudad_residencia = fields.Str()
    antiguedad_residencia = fields.Int()
    contrasena = fields.Str()
    id_plan_subscripcion = fields.UUID()
