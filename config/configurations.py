# voorbeeld van de Flask megatutorial
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

import os
from dotenv import load_dotenv


# Nieuwe REPO voor schema en definitiebestand:
IV3_REPO_PATH = "https://raw.github.com/statistiekcbs/iv3_definities/master/"
IV3_SCHEMA_FILE = "iv3_data_schema_v{}.json"
IV3_DEF_FILE = "iv3_definities_{}_{}.json"

# JSON bestand-controle gebeurt extern via Open State Foundation (OSF) API aanroep of niet.
EXTERNE_CONTROLE = False

OSF_API_GEEF_TOTALEN_UITKOMST_URL = 'https://cbs.openstate.eu/geef_totalen_uitkomst'
OSF_API_GEEF_FOUTEN_URL = 'https://cbs.openstate.eu/geef_fouten'

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# define several configurations
# default, development, test, production
class Config_Master(object):
    APP_ENV = 'master'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'master_key'


class Config_Default(object):
    APP_ENV = 'default'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_key'


class Config_Development(object):
    APP_ENV = 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development_key'


class Config_DebugJavascript(object):
    APP_ENV = 'debugjavascript'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'debugjavascript_key'


class Config_Test(object):
    APP_ENV = 'test'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_key'


class Config_Production(object):
    APP_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production_key'
