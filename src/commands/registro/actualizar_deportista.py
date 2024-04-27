import os
from sqlalchemy import update
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.plan_subscripcion import PlanSubscripcion
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist
from src.models.deportista import Deportista

logger = logging.getLogger(__name__)


class ActualizarDeportista(BaseCommand):
    def __init__(self, **info_deportista):
        super().__init__()
        self.__dict__.update(info_deportista)
        self.info_deportista = info_deportista

    def execute(self):
        logger.info(f'Commando: Actualizando Deportista: {self.email}')

        # Validar que deportista exista
        deportista = db_session.query(Deportista).filter(
            Deportista.email == self.email).first()

        if deportista is None:
            logger.error("Deportista No Existe")
            raise BadRequest
        else:
            #record = Deportista(**self.info_deportista)
            #db_session.add(record)
            #deportista.id_plan_subscripcion = self.id_plan_subscripcion

            deportista.nombre = self.nombre
            deportista.apellido = self.apellido
            deportista.tipo_identificacion = self.tipo_identificacion
            deportista.numero_identificacion = self.numero_identificacion
            deportista.genero = self.genero
            deportista.edad = self.edad
            deportista.peso = self.peso
            deportista.altura = self.altura
            deportista.pais_nacimiento = self.pais_nacimiento
            deportista.ciudad_nacimiento = self.ciudad_nacimiento
            deportista.pais_residencia = self.pais_residencia
            deportista.ciudad_residencia = self.ciudad_residencia
            deportista.antiguedad_residencia = self.antiguedad_residencia

            db_session.commit()
            response = {
                'message': 'success',
                'id_deportista': deportista.id
            }

        return response
