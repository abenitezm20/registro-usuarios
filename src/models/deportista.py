import enum
from datetime import datetime
from sqlalchemy import Column, Integer, Enum, String, Float
from .model import Model
from .db import Base


class Tipo_IdentificacionEnum(str, enum.Enum):
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
    tipo_identificacion = Column(Enum(Tipo_IdentificacionEnum))
    numero_identificacion = Column(Integer)                                
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


    def __init__(self, nombre, apellido, tipo_identificacion, numero_identificacion, email, genero, edad, peso, altura, pais_nacimiento, ciudad_nacimiento, pais_residencia, ciudad_residencia, antiguedad_residencia, contrasena):
        Model.__init__(self)
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.email = email
        self.genero = genero
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.pais_nacimiento = pais_nacimiento
        self.ciudad_nacimiento = ciudad_nacimiento
        self.pais_residencia = pais_residencia
        self.ciudad_residencia = ciudad_residencia
        self.antiguedad_residencia = antiguedad_residencia
        self.contrasena = contrasena
        