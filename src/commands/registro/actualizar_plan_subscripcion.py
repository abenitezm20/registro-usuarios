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


class ActualizarPlanSubscripcion(BaseCommand):
    def __init__(self, **info_deportista):
        super().__init__()
        self.__dict__.update(info_deportista)
        self.info_deportista = info_deportista

    def execute(self):
        logger.info(f'Actualizando Plan Subscripcion: {self.email}')

        # Validar que deportista exista
        deportista = db_session.query(Deportista).filter(
            Deportista.email == self.email).first()

        if deportista is None:
            logger.error("Deportista No Existe")
            raise BadRequest
        else:
            deportista.id_plan_subscripcion = self.id_plan_subscripcion
            db_session.commit()
            response = {
                'message': 'success'
            }

        return response
