import logging

from src.commands.base_command import BaseCommand
from src.models.deporte import Deporte
from src.models.deporte_deportista import DeporteDeportista
from src.models.db import db_session
from src.errors.errors import BadRequest
from sqlalchemy import delete

logger = logging.getLogger(__name__)


class ActualizarDeporteDeportista(BaseCommand):
    def __init__(self, info_deporte_deportista, id_deportista: str):
        super().__init__()
        self.__dict__.update(info_deporte_deportista)
        self.info_deporte_deportista = info_deporte_deportista
        self.id_deportista = id_deportista

    def execute(self):

        with db_session() as session:

            # Se eliminan las asignaciones existentes
            dele = delete(DeporteDeportista).where(
                DeporteDeportista.id_deportista == self.id_deportista)
            session.execute(dele)
            session.commit()

            logger.info("Se asignan nuevos deportes: " + str(
                self.info_deporte_deportista['deportes']) + " al deportista: " + self.id_deportista)
            # se asignan los nuevos deportes
            for deporte in self.info_deporte_deportista['deportes']:

                if deporte.get('atletismo'):
                    if deporte['atletismo'] == "1":
                        self._procesar_atletismo(session, self.id_deportista)
                    else:
                        print("Atletismo no es seleccionado")
                elif deporte.get('ciclismo'):
                    if deporte['ciclismo'] == "1":
                        self._procesar_ciclismo(session, self.id_deportista)
                    else:
                        print("Ciclismo no es seleccionado")
            response = {
                'message': 'success'
            }
            return response

    def _procesar_atletismo(self, session, id_deportista):
        deporte_bd = session.query(Deporte).filter(
            Deporte.nombre == "Atletismo").first()
        id_deporte = deporte_bd.id

        if id_deporte is None:
            logger.error("Deporte no encontrado")
            raise BadRequest
        else:
            record = DeporteDeportista(
                id_deporte=id_deporte, id_deportista=id_deportista)
            session.add(record)
            session.commit()

    def _procesar_ciclismo(self, session, id_deportista):
        deporte_bd = session.query(Deporte).filter(
            Deporte.nombre == "Ciclismo").first()
        id_deporte = deporte_bd.id

        if id_deporte is None:
            logger.error("Deporte no encontrado")
            raise BadRequest
        else:
            record = DeporteDeportista(
                id_deporte=id_deporte, id_deportista=id_deportista)
            session.add(record)
            session.commit()
