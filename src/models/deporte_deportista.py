import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from .model import Model
from .db import Base
from sqlalchemy.orm import Mapped, relationship


class DeporteDeportista(Model, Base):
    __tablename__ = "deporte_deportista"
    id_deporte = Column(UUID(as_uuid=True))

    id_deportista = Column(UUID(as_uuid=True), ForeignKey('deportista.id'), primary_key=True)
    deportista: Mapped['Deportista'] = relationship("Deportista", backref="deportesdeportista")


    def __init__(self, **info_deporte_deportista):
        Model.__init__(self)
        self.__dict__.update(info_deporte_deportista)
