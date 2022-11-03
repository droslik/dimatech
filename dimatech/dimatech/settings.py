import os

from environs import Env
from sanic_envconfig import EnvConfig

env = Env()
env.read_env()


class Settings(EnvConfig):
    DEBUG: bool = env('DEBUG') == 'True'
    HOST: str = env('HOST')
    PORT: int = env('PORT')
    SECRET: str = env('SECRET')
    JWT_SECRET_KEY: str = env('SECRET_KEY')
    ALGORITHM: str = env('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env('ACCESS_TOKEN_EXPIRE_MINUTES')
    PRIVATE_KEY: str = env('PRIVATE_KEY')
    # postgres settings
    POSTGRESQL_NAME: str = env('POSTGRESQL_NAME')
    POSTGRESQL_USER: str = env('POSTGRESQL_USER')
    POSTGRESQL_PASSWORD: str = os.getenv('POSTGRESQL_PASSWORD')
    POSTGRESQL_HOST: str = os.getenv('POSTGRESQL_HOST')
    POSTGRESQL_PORT: int = env('POSTGRESQL_PORT')






