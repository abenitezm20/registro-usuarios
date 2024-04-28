import json
import uuid
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deporte_deportista import DeporteDeportista
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum
from sqlalchemy import delete

from src.models.plan_subscripcion import PlanSubscripcion

fake = Faker()
logger = logging.getLogger(__name__)
token = ""


@pytest.fixture(scope="class")
def setup_data():
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
        'deportes' : [ {"atletismo": 1}, {"ciclismo": 0}]
    }
    deportista_random = Deportista(**info_deportista)
    db_session.add(deportista_random)
    db_session.commit()

    info_deporte = {
        'nombre': 'Atletismo',
    }
    deporte_random = Deporte(**info_deporte)
    db_session.add(deporte_random)
    db_session.commit()

    info_plan_subscripcion = {
        'nombre': 'Intermedio',
    }
    planSubs_random = PlanSubscripcion(**info_plan_subscripcion)
    db_session.add(planSubs_random)
    db_session.commit()

    yield {
        'deportista': deportista_random,
        'deportes': deporte_random,
        'plan_subscripcion': planSubs_random,
    }
    
    db_session.delete(deporte_random)
    db_session.delete(planSubs_random)
    db_session.delete(deportista_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestActualizarPlanSubscripcion():
    
    @patch('requests.post')
    def test_actualizar_plan_subscripcion_exitoso(self, mock_post, setup_data):

        with app.test_client() as test_client:
            #Mock para obtener el token
            deportista: Deportista = setup_data['deportista']
            mock_response_1 = MagicMock()
            mock_response_1.status_code = 200
            mock_response_1.json.return_value = {
                'token_valido': True, 
                'email': deportista.email,
                'subscripcion': deportista.id_plan_subscripcion,
                'tipo_usuario': 'deportista'
                }
            mock_post.return_value = mock_response_1

            headers = {'Authorization': 'Bearer 123'}

            body = {
                "plan_subscripcion": setup_data['plan_subscripcion'].nombre
            }
        
            response = test_client.put(
                '/registro-usuarios/registro/deportistaupgrade', headers=headers, json=body, follow_redirects=True)
            response_json = json.loads(response.data)

            assert response.status_code == 200