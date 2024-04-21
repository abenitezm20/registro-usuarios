import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.deportista import Deportista, DeportistaSchema


logger = logging.getLogger(__name__)


class ObtenerDeportista(BaseCommand):
    def __init__(self, **info):
        if info.get('email') is None:
            logger.error("email no puede ser vacio o nulo")
            raise BadRequest

        self.email = info.get('email')

    def execute(self):
        logger.info("Obteniendo deportista: " + self.email)
        deportista = Deportista.query.filter_by(email=self.email).first()

        if deportista is None:
            return None

        else:
            schema = DeportistaSchema()
            return schema.dump(deportista)
