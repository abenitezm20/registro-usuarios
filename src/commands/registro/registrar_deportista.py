import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.deportista import Deportista
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist

logger = logging.getLogger(__name__)


class RegistrarDeportista(BaseCommand):
    def __init__(self, **info_deportista):
        super().__init__()
        self.__dict__.update(info_deportista)
        self.info_deportista = info_deportista

    def execute(self):
        logger.info(f'Validando Información: {self.email}')

        # Validar que la información no sea nula
        if self.nombre is None or self.apellido is None or self.tipo_identificacion is None or self.numero_identificacion is None or self.email is None or self.genero is None or self.edad is None or self.peso is None or self.altura is None or self.pais_nacimiento is None or self.ciudad_nacimiento is None or self.pais_residencia is None or self.ciudad_residencia is None or self.antiguedad_residencia is None or self.contrasena is None:
            logger.error("Información invalida")
            raise BadRequest

        # Validar que la información no sea vacía
        if self.nombre == "" or self.apellido == "" or self.tipo_identificacion == "" or self.numero_identificacion == "" or self.email == "" or self.genero == "" or self.edad == "" or self.peso == "" or self.altura == "" or self.pais_nacimiento == "" or self.ciudad_nacimiento == "" or self.pais_residencia == "" or self.ciudad_residencia == "" or self.antiguedad_residencia == "" or self.contrasena == "":
            logger.error("Información invalida")
            raise BadRequest

        # Validar que la identificación no sea mayor a 15 dígitos
        if len(str(self.numero_identificacion)) > 15:
            logger.error("Número de identificación mayor a 15 digitos")
            raise BadRequest

        # Validar que la edad no sea mayor a 3 dígitos
        if len(str(self.edad)) > 3:
            logger.error("Edad mayor a 3 digitos")
            raise BadRequest

        # Validar que el peso no sea mayor a 3 dígitos y 1 decimal
        if len(str(self.peso)) > 5:
            logger.error("Peso mayor a 3 digitos y 1 decimal")
            raise BadRequest

        # Validar que la altura no sea mayor a 3 dígitos
        if len(str(self.altura)) > 3:
            logger.error("Altura mayor a 3 digitos")
            raise BadRequest

        # Validar que el tiempo de residencia no sea mayor a 3 dígitos
        if len(str(self.antiguedad_residencia)) > 3:
            logger.error("Tiempo Residencia mayor a 3 digitos")
            raise BadRequest

        # Validar que deportista no exista
        deportista = db_session.query(Deportista).filter(
            Deportista.email == self.email).first()

        if deportista is not None:
            logger.error("Deportista Ya Existe")
            raise UserAlreadyExist
        else:
            logger.info(f"Registrando Deportista: {self.email}")
            record = Deportista(**self.info_deportista)
            db_session.add(record)
            db_session.commit()
            deportistanuevo = db_session.query(Deportista).filter(Deportista.email == self.email).first()
            response = {
                'message': 'success',
                'id_deportista': str(deportistanuevo.id)
            }

        return response
