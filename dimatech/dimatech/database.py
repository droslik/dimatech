from sqlalchemy import create_engine
from settings import Settings
from databases import Database
import models

SQLALCHEMY_DATABASE_URL = f'postgresql://' \
                          f'{Settings.POSTGRESQL_USER}:' \
                          f'{Settings.POSTGRESQL_PASSWORD}@' \
                          f'{Settings.POSTGRESQL_HOST}:' \
                          f'{Settings.POSTGRESQL_PORT}/' \
                          f'{Settings.POSTGRESQL_NAME}'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
        )

database = Database(SQLALCHEMY_DATABASE_URL)

models.metadata.create_all(engine)


