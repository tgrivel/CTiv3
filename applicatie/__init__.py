import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        # read config file from the instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load config object passed on start-up
        app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from applicatie.main import bp as main_bp
    app.register_blueprint(main_bp)

    #print('Running with configuration: ' + app.config['APP_ENV'])
    return app
