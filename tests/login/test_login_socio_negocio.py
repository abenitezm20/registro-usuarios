import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.socio_negocio import SocioNegocio, Tipo_IdentificacionSocioEnum


fake = Faker()
logger = logging.getLogger(__name__)

URL_LOGIN_SOCIO_NEGOCIO = 'registro-usuarios/login/socio-negocio'


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestLoginSocioNegocio")

    socio_negocio_random = SocioNegocio(
        nombre=fake.name(),
        tipo_identificacion=fake.random_element(elements=(
            tipo_identificacion.value for tipo_identificacion in Tipo_IdentificacionSocioEnum)),
        numero_identificacion=fake.random_int(min=1000000, max=9999999),
        email=fake.email(),
        contrasena=fake.password(),
    )

    db_session.add(socio_negocio_random)
    db_session.commit()
    logger.info('Socio negocio creado: ' + socio_negocio_random.email)
    yield socio_negocio_random
    logger.info("Fin TestLoginSocioNegocio")
    db_session.delete(socio_negocio_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestLoginSocioNegocio():

    def test_login_sin_contrasena(self):
        with app.test_client() as test_client:
            body = {"email": fake.email()}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_contrasena_corta(self):
        with app.test_client() as test_client:
            body = {"email": fake.email(), "contrasena": "123"}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_sin_email(self):
        with app.test_client() as test_client:
            body = {"contrasena": fake.password()}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_email_invalido(self):
        with app.test_client() as test_client:
            body = {"email": "email_invalido", "contrasena": fake.password()}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_deportista_no_encontrado(self):
        with app.test_client() as test_client:
            body = {"email": fake.email(), "contrasena": fake.password()}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 404
            assert response_json['error'] == 'resource_not_found'

    def test_login_contrasena_invalida(self, setup_data: SocioNegocio):
        with app.test_client() as test_client:
            body = {"email": setup_data.email, "contrasena": fake.password()}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 401
            assert response_json['error'] == 'unauthorized'

    @patch('requests.post')
    def test_login_exitoso(self, mock_post, setup_data: SocioNegocio):
        with app.test_client() as test_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'token': '123456'}
            mock_post.return_value = mock_response

            body = {"email": setup_data.email,
                    "contrasena": setup_data.contrasena}

            response = test_client.post(URL_LOGIN_SOCIO_NEGOCIO, json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'token' in response_json
            assert response_json['token'] is not None
