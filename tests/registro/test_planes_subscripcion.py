import json
import logging
import pytest

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum
from src.models.detalle_subscripcion import DetalleSubscripcion
from src.models.plan_subscripcion import PlanSubscripcion
from unittest.mock import patch, MagicMock


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    with db_session() as session:
        # Plan de subscripcion
        info_plan = {
            'nombre': 'Plan Basico',
        }

        plan_subscripcion = PlanSubscripcion(**info_plan)
        session.add(plan_subscripcion)
        session.commit()

        info_detalle = {
            'id_plan_subscripcion': plan_subscripcion.id,
            'beneficios': 'Beneficio 1|Beneficio 2|Beneficio 3',
        }

        # Detalle de subscripcion
        detalle_subscripcion = DetalleSubscripcion(**info_detalle)
        session.add(detalle_subscripcion)
        session.commit()

        # Deportista
        info_deportista = {
            'nombre': fake.name(),
            'apellido': fake.name(),
            'tipo_identificacion': fake.random_element(elements=(
                tipo_identificacion.value for tipo_identificacion in TipoIdentificacionEnum)),
            'numero_identificacion': fake.random_int(min=1000000, max=999999999),
            'email': fake.email(),
            'genero': fake.random_element(elements=(genero.value for genero in GeneroEnum)),
            'edad': fake.random_int(min=18, max=100),
            'peso': fake.pyfloat(3, 1, positive=True),
            'altura': fake.random_int(min=140, max=200),
            'pais_nacimiento': fake.country(),
            'ciudad_nacimiento': fake.city(),
            'pais_residencia': fake.country(),
            'ciudad_residencia': fake.city(),
            'antiguedad_residencia': fake.random_int(min=0, max=10),
            'contrasena': fake.password(),
            'id_plan_subscripcion': plan_subscripcion.id,
            'deportes': [{"atletismo": "1"}, {"ciclismo": "0"}]
        }
        deportista_random = Deportista(**info_deportista)
        session.add(deportista_random)
        session.commit()

        yield {
            'id_plan_subscripcion': plan_subscripcion.id,
            'id_detalle_subscripcion': detalle_subscripcion.id,
            'id_deportista': deportista_random.id,
            'email_deportista': deportista_random.email,
        }

        session.delete(deportista_random)
        session.delete(detalle_subscripcion)
        session.delete(plan_subscripcion)
        session.commit()


@pytest.mark.usefixtures("setup_data")
class TestActualizarDeportista():

    def test_obtener_planes_subscripcion_exitoso(self, setup_data):
        with app.test_client() as test_client:

            response = test_client.get(
                '/registro-usuarios/registro/obtener_planes_subscripion')
            response_json = json.loads(response.data)

            assert response.status_code == 200

    @patch('requests.post')
    def test_obtener_planes_subscripion_actual_exitoso(self, mock_post, setup_data):

        with app.test_client() as test_client:

            # Mock para obtener el token
            mock_response_1 = MagicMock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = {
                'token_valido': True,
                'email': setup_data['email_deportista'],
                'subscripcion': setup_data['id_plan_subscripcion'],
                'tipo_usuario': 'deportista'
            }
            mock_post.return_value = mock_response_1

            headers = {'Authorization': 'Bearer 123'}

            response = test_client.get(
                '/registro-usuarios/registro/obtener_planes_subscripion/actual', headers=headers)
            response_json = json.loads(response.data)

            assert response.status_code == 200
