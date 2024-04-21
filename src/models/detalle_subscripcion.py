import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from .model import Model
from .db import Base
from sqlalchemy.orm import relationship


class DetalleSubscripcion(Model, Base):
    __tablename__ = "detalle_subscripcion"
    id_plan_subscripcion = Column(UUID, ForeignKey('plan_subscripcion.id'))
    plan_subscripcion = relationship('PlanSubscripcion')
    beneficios = Column(String(300))

    def __init__(self, **info_detalle_subscripcion):
        Model.__init__(self)
        self.__dict__.update(info_detalle_subscripcion)
