import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from .model import Model
from sqlalchemy.orm import relationship
from .db import Base


class PlanSubscripcion(Model, Base):
    __tablename__ = "plan_subscripcion"
    nombre = Column(String(30))

    def __init__(self, **info_plan_subscripcion):
        Model.__init__(self)
        self.__dict__.update(info_plan_subscripcion)


