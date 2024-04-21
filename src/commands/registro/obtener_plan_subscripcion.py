import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.detalle_subscripcion import DetalleSubscripcion
from src.models.plan_subscripcion import PlanSubscripcion
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist
from src.utils.str_utils import str_none_or_empty

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


class ObtenerPlanesSubscripcion(BaseCommand):
    def __init__(self):
        pass

    def execute(self):
        logger.info(f"Buscando Planes de Subscripcion")
        respuesta = []
        obtenerPlanesSubscripcion  = db_session.query(PlanSubscripcion).all()
        if obtenerPlanesSubscripcion is None:
            logger.error("Planes no encontrados")
            raise BadRequest
        else:
            for planes in obtenerPlanesSubscripcion:
                beneficios = db_session.query(DetalleSubscripcion).filter(DetalleSubscripcion.id_plan_subscripcion == planes.id).first()

                if beneficios is None:
                    logger.error("Beneficios no encontrados")
                    raise BadRequest
                else:
                    split_beneficios = beneficios.beneficios.split('|')
                    beneficiosOrder = []
                    for i in range(len(split_beneficios)):
                        beneficios_temp = {
                            'beneficios': split_beneficios[i],
                            'id_detalle_subscripcion': i+1
                        }
                        beneficiosOrder.append(beneficios_temp)

                    resp_tmp = {
                        'id_plan_subscripcion': planes.id,
                        'nombre': planes.nombre,
                        'beneficios': beneficiosOrder
                    }
                    respuesta.append(resp_tmp)
            return respuesta       

