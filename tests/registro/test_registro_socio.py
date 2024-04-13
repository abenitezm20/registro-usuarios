import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.socio_negocio import SocioNegocio, TipoIdentificacionSocioEnum


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    socio_random = SocioNegocio(
        nombre=fake.name(),
        tipo_identificacion=fake.random_element(elements=(
            tipo_identificacion.value for tipo_identificacion in TipoIdentificacionSocioEnum)),
        numero_identificacion=fake.random_int(min=1000000, max=999999999),
        email=fake.email(),
        contrasena=fake.password())

    yield socio_random

    tmp_socio = db_session.query(SocioNegocio).filter(
        SocioNegocio.email == socio_random.email).first()
    if tmp_socio is not None:
        db_session.delete(tmp_socio)
        db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestRegistroSocio():

    def test_registro_socio_exitoso(self, setup_data: SocioNegocio):
        '''Prueba de crear un socio exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data.nombre,
                "tipo_identificacion": setup_data.tipo_identificacion,
                "numero_identificacion": setup_data.numero_identificacion,
                "email": setup_data.email,
                "contrasena": setup_data.contrasena
            }

            response = test_client.post(
                'registro-usuarios/registro/socios', json=body)

            assert response.status_code == 200
            assert response.json['message'] == 'success'

    def test_registro_socio_existente(self, setup_data: SocioNegocio):
        '''Prueba de crear un socio exitosamente'''
        with app.test_client() as test_client:
            body = {
                "nombre": setup_data.nombre,
                "tipo_identificacion": setup_data.tipo_identificacion,
                "numero_identificacion": setup_data.numero_identificacion,
                "email": setup_data.email,
                "contrasena": setup_data.contrasena
            }

            response = test_client.post(
                'registro-usuarios/registro/socios', json=body)

            assert response.status_code == 432

    def test_registro_socio_campos_vacios(self):
        '''Prueba de crear un socio con campos vacios'''
        with app.test_client() as test_client:
            body = {
                "nombre": "",
                "tipo_identificacion": "",
                "numero_identificacion": "",
                "email": "",
                "contrasena": ""
            }

            response = test_client.post(
                'registro-usuarios/registro/socios', json=body)

            assert response.status_code == 400
