import os
from applicatie import create_app
from config import configurations
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

config = ''
# choose a configuration based on FLASK_ENV
if os.environ.get('FLASK_ENV') == 'default':
    config = configurations.Config_Default()
elif os.environ.get('FLASK_ENV') == 'development':
    config = configurations.Config_Development()
elif os.environ.get('FLASK_ENV') == 'test':
    config = configurations.Config_Test()
elif os.environ.get('FLASK_ENV') == 'production':
    config = configurations.Config_Production()

if not config == '':
    # create app with selected configuration
    app = create_app(config)
else:
    # create ap without configuration
    app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
