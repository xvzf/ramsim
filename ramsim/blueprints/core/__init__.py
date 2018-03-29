from ...util.framework.blueprint import create_blueprint

blueprint = create_blueprint("core", __name__)

from . import views
