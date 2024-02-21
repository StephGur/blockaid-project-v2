import flask_cors
from flask import Flask, Blueprint

import config


def make_app(app_config: config.BaseConfig) -> Flask:
    app_config = app_config or config.BLOCKAID_CONFIG
    app = Flask(__name__)
    app.config.from_object(app_config)
    flask_cors.CORS(app)

    with app.app_context():
        _register_blueprints(app)

    return app


def _register_blueprints(app):
    from bloackaid.resource import create_api_blueprints
    main_bp: Blueprint = create_api_blueprints()
    app.register_blueprint(main_bp)
