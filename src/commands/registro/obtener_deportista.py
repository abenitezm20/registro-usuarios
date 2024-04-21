import logging

from src.commands.base_command import BaseCommand
from src.models.deportista import Deportista, DeportistaSchema


logger = logging.getLogger(__name__)


class ObtenerDeportista(BaseCommand):
    def __init__(self, id_deportista: str):
        self.id_deportista = id_deportista

    def execute(self):
        logger.info("Obteniendo deportista con id " + self.id_deportista)
        deportista = Deportista.query.filter_by(id=self.id_deportista).first()

        if deportista is None:
            return None

        else:
            schema = DeportistaSchema()
            return schema.dump(deportista)
