from sanic import Sanic
from sanic_session import Session
from settings import Settings
from urls import all_urls
from database import database


app = Sanic("dimatech")

session = Session(app)
app.ctx.db = database


@app.listener('after_server_start')
async def connect_to_db(*args, **kwargs):
    await app.ctx.db.connect()


@app.listener('after_server_stop')
async def disconnect_from_db(*args, **kwargs):
    await app.ctx.db.disconnect()

for url in all_urls:
    app.add_route(uri=url['uri'], handler=url['handler'], methods=url['methods'])


def init():

    Settings()
    app.run(host=Settings.HOST, port=Settings.PORT, auto_reload=Settings.DEBUG)


