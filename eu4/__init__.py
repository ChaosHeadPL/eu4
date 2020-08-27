import logging.config
import os
from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

BASE_DIR=os.path.dirname(__file__)


app = Flask(__name__)
api = Api(version="1.0", title="EU4 API")

app.config.from_pyfile(os.path.join(BASE_DIR, "config.py"))

# db = SQLAlchemy(app)

blueprint = Blueprint("api", __name__, url_prefix="/api")
api.init_app(blueprint)
app.register_blueprint(blueprint)

# # disable warkezeug server messages:
log = logging.getLogger('werkzeug')
log.disabled = True

# # init logger:
logging_conf_path = os.path.join(BASE_DIR, "logging.conf")
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger("logger_root")
if app.config.get("LOG_LEVEL"):
    log.info(f"LOG_LEVEL set to {app.config.get('LOG_LEVEL')}")
    log.debug("TEST")
    log.setLevel=app.config.get("LOG_LEVEL")


from eu4 import routes  # pylint: disable=no-member
