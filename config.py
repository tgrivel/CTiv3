# voorbeeld van de Flask megatutorial
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
