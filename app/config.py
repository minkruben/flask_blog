import os


class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:Gilchrist1~@localhost:5432/blog_db'
