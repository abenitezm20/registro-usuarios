import logging
from flask import Blueprint, request, jsonify, make_response
from src.commands.login.login_deportista import LoginDeportista
from src.commands.login.login_socio_negocio import LoginSocioNegocio


logger = logging.getLogger(__name__)
login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/deportista', methods=['POST'])
def login_deportista():
    body = request.get_json()

    result = LoginDeportista(
        body.get('email', None),
        body.get('contrasena', None),
    ).execute()

    return make_response(jsonify(result), 200)


@login_blueprint.route('/socio-negocio', methods=['POST'])
def login_socio_negocio():
    body = request.get_json()

    result = LoginSocioNegocio(
        body.get('email', None),
        body.get('contrasena', None),
    ).execute()

    return make_response(jsonify(result), 200)
