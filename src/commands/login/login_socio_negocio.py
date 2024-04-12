import logging
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, ResourceNotFound, Unauthorized
from src.utils.str_utils import str_none_or_empty, is_email
from src.utils.seguridad_utils import get_token
from src.models.socio_negocio import SocioNegocio
from src.models.db import db_session


logger = logging.getLogger(__name__)


class LoginSocioNegocio(BaseCommand):

    def __init__(self, email: str, contrasena: str):
        if str_none_or_empty(contrasena) or len(contrasena) < 8:
            logger.error("Contrasena invalida")
            raise BadRequest

        if str_none_or_empty(email) or (is_email(email) is False):
            logger.error("Email invalido")
            raise BadRequest

        self.email = email
        self.contrasena = contrasena

    def execute(self):
        logger.info(f"Login socio negocio: {self.email}")

        socio_negocio = db_session.query(SocioNegocio).filter(
            SocioNegocio.email == self.email).first()

        if socio_negocio is None:
            logger.error("Socio de negocio no encontrado")
            raise ResourceNotFound

        if socio_negocio.contrasena != self.contrasena:
            logger.error("Contrasena invalida")
            raise Unauthorized

        token = get_token(self.email)
        return {'token': token}
