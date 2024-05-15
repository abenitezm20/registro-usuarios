import logging
import uuid

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deporte_deportista import DeporteDeportista
from src.models.deportista import Deportista, DeportistaSchema


logger = logging.getLogger(__name__)


class ObtenerDeporteDeportista(BaseCommand):
    def __init__(self, deportista_id: uuid):
        if deportista_id is None:
            logger.error(
                "ID es obtenerDeporteDeportista no puede ser vacio o nulo")
            raise BadRequest
        self.deportista_id = deportista_id

    def execute(self):
        logger.info("Obteniendo deportes de deportista")
        deporte_deportista = DeporteDeportista.query.filter_by(
            id_deportista=self.deportista_id).all()

        if deporte_deportista is None:
            return None

        else:
            with db_session() as session:

                response = []
                for deporte in deporte_deportista:
                    deporte_seleccionado = session.query(Deporte).filter_by(
                        id=deporte.id_deporte).first()

                    response.append(deporte_seleccionado.nombre)
                return response
