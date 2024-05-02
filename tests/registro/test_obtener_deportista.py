import json
import pytest
import logging
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.deporte_deportista import DeporteDeportista
from src.models.deportista import Deportista, GeneroEnum, TipoIdentificacionEnum


fake = Faker()
logger = logging.getLogger(__name__)
token = ""


@pytest.fixture(scope="class")
def setup_data():
    with db_session() as session:
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
            'deportes' : [ {"atletismo": 1}, {"ciclismo": 1}]
        }

        deportista_random = Deportista(**info_deportista)
        session.add(deportista_random)
        session.commit()

        yield {
            'deportista': deportista_random,
        }
    
        session.delete(deportista_random)
        session.commit()


@pytest.mark.usefixtures("setup_data")
class TestObtenerDeportista():
    
    @patch('requests.post')
    def test_obtener_deportista_exitoso(self, mock_post, setup_data):
        '''Prueba de obtener un deportista exitosamente'''
        with app.test_client() as test_client:
            
            deportista: Deportista = setup_data['deportista']
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 
                'email': deportista.email,
                'subscripcion': deportista.id_plan_subscripcion,
                'tipo_usuario': 'deportista'
                }
            mock_post.return_value = mock_response
        
            endpoint_deportista = "registro-usuarios/registro/deportista"
            headers = {'Authorization': 'Bearer 123'}
            resultado_obtener_deportista = test_client.get(endpoint_deportista, headers=headers)
            assert resultado_obtener_deportista.status_code == 200