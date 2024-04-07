import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.deportista import Deportista
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist

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
        logging.info(f'Validando Información: {self.email}')

        # Validar que la información no sea nula
        if self.nombre is None or self.apellido is None or self.tipo_identificacion is None or self.numero_identificacion is None or self.email is None or self.genero is None or self.edad is None or self.peso is None or self.altura is None or self.pais_nacimiento is None or self.ciudad_nacimiento is None or self.pais_residencia is None or self.ciudad_residencia is None or self.antiguedad_residencia is None or self.contrasena is None:
            logging.error("Información invalida")
            raise BadRequest
        
        # Validar que deportista no exista
        deportista = db_session.query(Deportista).filter(
            Deportista.email == self.email).first()

        if deportista is not None:
            logging.error("Deportista Ya Existe")
            raise UserAlreadyExist
        else:
            logging.info(f'Registrando Deportista')
            record = Deportista(self.nombre, self.apellido, self.tipo_identificacion, self.numero_identificacion, self.email, self.genero, self.edad, self.peso, self.altura, self.pais_nacimiento, self.ciudad_nacimiento, self.pais_residencia, self.ciudad_residencia, self.antiguedad_residencia, self.contrasena)
            db_session.add(record)
            db_session.commit()
            response = {
                'message': 'success'
            }

        return response