from flask import Blueprint

bp_api = Blueprint('bp_api', __name__)
bp_auth = Blueprint('bp_auth', __name__)

from api2.blueprints import posts, auth
