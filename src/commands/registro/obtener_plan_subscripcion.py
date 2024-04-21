import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.plan_subscripcion import PlanSubscripcion
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist

logger = logging.getLogger(__name__)


class ObtenerPlanSubscripcion(BaseCommand):
    def __init__(self, nombreSubscripcion: str):
        self.nombreSubscripcion = nombreSubscripcion

    def execute(self):
        logger.info(f"Buscando Plan: {self.nombreSubscripcion}")

        plan = db_session.query(PlanSubscripcion).filter(
            PlanSubscripcion.nombre == self.nombreSubscripcion).first()
        
        if plan is None:
            logger.error("Plan no encontrado")
            raise BadRequest
        else:
            return plan.id
