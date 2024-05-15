import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.deportista import Deportista
from src.models.detalle_subscripcion import DetalleSubscripcion
from src.models.plan_subscripcion import PlanSubscripcion
from src.models.db import db_session
from src.errors.errors import BadRequest


logger = logging.getLogger(__name__)


class ObtenerPlanSubscripcion(BaseCommand):
    def __init__(self, nombre_subscripcion: str):
        self.nombre_subscripcion = nombre_subscripcion

    def execute(self):
        logger.info(f"Buscando Plan: {self.nombre_subscripcion}")

        plan = db_session.query(PlanSubscripcion).filter(
            PlanSubscripcion.nombre == self.nombre_subscripcion).first()

        if plan is None:
            logger.error("Plan no encontrado")
            raise BadRequest
        else:
            return plan.id


class ObtenerPlanesSubscripcion(BaseCommand):
    def __init__(self):
        '''
        Constructor de la clase ObtenerPlanesSubscripcion
        '''
        pass

    def execute(self):
        logger.info("Buscando Planes de Subscripcion")

        with db_session() as session:

            respuesta = []
            obtener_planes_subscripcion = session.query(PlanSubscripcion).all()
            if obtener_planes_subscripcion is None:
                logger.error("Planes no encontrados")
                raise BadRequest
            else:
                for planes in obtener_planes_subscripcion:
                    beneficios = session.query(DetalleSubscripcion).filter(
                        DetalleSubscripcion.id_plan_subscripcion == planes.id).first()

                    if beneficios is None:
                        logger.error("Beneficios no encontrados")
                        raise BadRequest
                    else:
                        split_beneficios = beneficios.beneficios.split('|')
                        beneficios_order = []
                        for i in range(len(split_beneficios)):
                            beneficios_temp = {
                                'beneficios': split_beneficios[i],
                                'id_detalle_subscripcion': i+1
                            }
                            beneficios_order.append(beneficios_temp)

                        resp_tmp = {
                            'id_plan_subscripcion': planes.id,
                            'nombre': planes.nombre,
                            'beneficios': beneficios_order
                        }
                        respuesta.append(resp_tmp)
                return respuesta


class ObtenerPlanesSubscripcionAccion(BaseCommand):
    def __init__(self, **info_deportista):
        super().__init__()
        self.__dict__.update(info_deportista)
        self.info_deportista = info_deportista

    def execute(self):
        logger.info("Buscando Planes de Subscripcion")

        obtener_planes_subscripcion = db_session.query(PlanSubscripcion).all()
        if obtener_planes_subscripcion is None:
            logger.error("Planes no encontrados")
            raise BadRequest

        deportista_actual = db_session.query(Deportista).filter(
            Deportista.email == self.info_deportista['email']).first()
        if deportista_actual is None:
            logger.error("Deportista no encontrado")
            raise BadRequest

        respuesta = []
        for planes in obtener_planes_subscripcion:
            beneficios = db_session.query(DetalleSubscripcion).filter(
                DetalleSubscripcion.id_plan_subscripcion == planes.id).first()

            if beneficios is None:
                logger.error("Beneficios no encontrados")
                raise BadRequest

            split_beneficios = beneficios.beneficios.split('|')
            beneficios_order = []
            for i in range(len(split_beneficios)):
                beneficios_temp = {
                    'beneficios': split_beneficios[i],
                    'id_detalle_subscripcion': i+1
                }
                beneficios_order.append(beneficios_temp)

            # Comparo si el plan es el actual o disponible
            resp_actual = []
            resp_disponible = []
            if planes.id == deportista_actual.id_plan_subscripcion:
                resp_actual = {
                    'id_plan_subscripcion': planes.id,
                    'nombre': planes.nombre,
                    'beneficios': beneficios_order
                }
            else:
                resp_disponible = {
                    'id_plan_subscripcion': planes.id,
                    'nombre': planes.nombre,
                    'beneficios': beneficios_order
                }

            if self.info_deportista['accion'] == 'actual' and resp_actual != []:
                respuesta.append(resp_actual)
            elif self.info_deportista['accion'] == 'disponible' and resp_disponible != []:
                respuesta.append(resp_disponible)

        return respuesta
