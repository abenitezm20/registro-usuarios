import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.deportista import Deportista
from src.models.db import db_session

logger = logging.getLogger(__name__)

class RegistrarDeportista(BaseCommand):
    def __init__(self, nombre, apellido, tipo_identificacion, numero_identificacion, email, genero, edad, peso, altura, pais_nacimiento, ciudad_nacimiento, pais_residencia, ciudad_residencia, antiguedad_residencia, contrasena):
        super().__init__()
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

    def execute(self):
        logging.info(f'Validando Información')
        

        logging.info(f'Registrando Deportista')
        record = Deportista(self.nombre, self.apellido, self.tipo_identificacion, self.numero_identificacion, self.email, self.genero, self.edad, self.peso, self.altura, self.pais_nacimiento, self.ciudad_nacimiento, self.pais_residencia, self.ciudad_residencia, self.antiguedad_residencia, self.contrasena)
        db_session.add(record)
        db_session.commit()
        response = {
            'message': 'success'
        }

        return response