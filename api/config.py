"""Classes used to config the behavior of Flask"""


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "some-secret-key-here!"


class TestConfig(Config):
    DEBUG = True
    TESTING = True


class DevConfig(Config):
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    SECRET_KEY = "qheiuqfiewfhiwuf1213fdAEask!sdlf;F#@(UE!2iejfuwaef"
