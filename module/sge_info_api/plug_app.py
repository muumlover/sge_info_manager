from aiohttp import web

from ac_api import PlugIn
from .data.controller import PerSudo
from .handle.api import *


async def init(plug):
    plug['persudo_rfq_inn'] = PerSudo('rfq', 'inn')


def get_plug():
    plug = PlugIn(on_startup=init)
    plug.middlewares.append(mid_project)
    plug.router.add_view(r'/{project}/{application}/db/{name:\w*}', DBInfo, name='api_db')
    plug.router.add_view(r'/{project}/{application}/cmd/{name:\w*}', CMDInfo, name='api_cmd')
    plug.router.add_view(r'/{project}/{application}/struct/{name:\w*}', STRUCTInfo, name='api_struct')
    return plug


if __name__ == '__main__':
    web.run_app(get_plug())
