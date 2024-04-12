import os
import jwt
import logging
from src.commands.base_command import BaseCommand
from src.models.socio_negocio import SocioNegocio
from src.models.db import db_session
from src.errors.errors import BadRequest, UserAlreadyExist

logger = logging.getLogger(__name__)

class RegistrarSocios(BaseCommand):
    def __init__(self, nombre, tipo_identificacion, numero_identificacion, email, contrasena):
        super().__init__()
        self.nombre = nombre
        self.tipo_identificacion = tipo_identificacion
        self.numero_identificacion = numero_identificacion
        self.email = email
        self.contrasena = contrasena

    def execute(self):
        logger.info(f'Validando Información: {self.email}')
       
        # Validar que la información no sea vacía
        if self.nombre == "" or self.tipo_identificacion == "" or self.numero_identificacion == "" or self.email == "" or self.contrasena == "":
            logger.error("Información invalida")
            raise BadRequest
        
        # Validar que Socio no exista
        socio = db_session.query(SocioNegocio).filter(SocioNegocio.email == self.email).first()

        if socio is not None:
            logger.error("Socio de Negocio Ya Existe")
            raise UserAlreadyExist
        else:
            logger.info(f"Registrando Socio de Negocio: {self.email}")
            record = SocioNegocio(self.nombre, self.tipo_identificacion, self.numero_identificacion, self.email, self.contrasena)
            db_session.add(record)
            db_session.commit()
            response = {
                'message': 'success'
            }

        return response