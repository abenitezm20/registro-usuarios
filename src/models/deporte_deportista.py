import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from .model import Model
from .db import Base
from sqlalchemy.orm import relationship


class DeporteDeportista(Model, Base):
    __tablename__ = "deporte_deportista"
    id_deporte = Column(UUID(as_uuid=True))

    id_deportista = Column(UUID, ForeignKey('deportista.id'))
    deportista = relationship('Deportista', cascade='all,delete')


    def __init__(self, **info_deporte_deportista):
        Model.__init__(self)
        self.__dict__.update(info_deporte_deportista)
