import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista, GeneroEnum, Tipo_IdentificacionEnum


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestLoginDeportista")

    deportista_random = Deportista(
        nombre=fake.name(),
        apellido=fake.name(),
        tipo_identificacion=fake.random_element(elements=(
            tipo_identificacion.value for tipo_identificacion in Tipo_IdentificacionEnum)),
        numero_identificacion=fake.random_int(min=1000000, max=9999999),
        email=fake.email(),
        genero=fake.random_element(
            elements=(genero.value for genero in GeneroEnum)),
        edad=fake.random_int(min=18, max=100),
        peso=fake.random_int(min=40, max=200),
        altura=fake.random_int(min=140, max=200),
        pais_nacimiento=fake.country(),
        ciudad_nacimiento=fake.city(),
        pais_residencia=fake.country(),
        ciudad_residencia=fake.city(),
        antiguedad_residencia=fake.random_int(min=0, max=10),
        contrasena=fake.password(),
    )

    db_session.add(deportista_random)
    db_session.commit()
    logger.info('Deportista creado: ' + deportista_random.email)
    yield deportista_random
    logger.info("Fin TestGetTestLoginDeportistaDeporte")
    db_session.delete(deportista_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestLoginDeportista():

    def test_login_sin_contrasena(self):
        with app.test_client() as test_client:
            body = {"email": fake.email()}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_contrasena_corta(self):
        with app.test_client() as test_client:
            body = {"email": fake.email(), "contrasena": "123"}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_sin_email(self):
        with app.test_client() as test_client:
            body = {"contrasena": fake.password()}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_email_invalido(self):
        with app.test_client() as test_client:
            body = {"email": "email_invalido", "contrasena": fake.password()}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 400
            assert response_json['error'] == 'bad_request'

    def test_login_deportista_no_encontrado(self):
        with app.test_client() as test_client:
            body = {"email": fake.email(), "contrasena": fake.password()}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 404
            assert response_json['error'] == 'resource_not_found'

    def test_login_contrasena_invalida(self, setup_data: Deportista):
        with app.test_client() as test_client:
            body = {"email": setup_data.email, "contrasena": fake.password()}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 401
            assert response_json['error'] == 'unauthorized'

    @patch('requests.post')
    def test_login_exitoso(self, mock_post, setup_data: Deportista):
        with app.test_client() as test_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'token': '123456'}
            mock_post.return_value = mock_response

            body = {"email": setup_data.email,
                    "contrasena": setup_data.contrasena}

            response = test_client.post(
                'registro-usuarios/login/deportista', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'token' in response_json
            assert response_json['token'] is not None
