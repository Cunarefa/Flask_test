from flask import Blueprint

bp_api = Blueprint('bp_api', __name__, template_folder='templates')

from api2.blueprints import posts, users
