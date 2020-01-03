from aiohttp import web

from ac_api import PlugIn
from .handle.view import *


async def init(plug):
    pass


def get_plug():
    plug = PlugIn(on_startup=init)
    plug.router.add_view(r'/{project}/{application}/db', CmdListView)
    plug.router.add_view(r'/{project}/{application}/db/{name:\w*}', CmdView)
    plug.router.add_view(r'/{project}/{application}/cmd', CmdListView)
    plug.router.add_view(r'/{project}/{application}/cmd/{command:\w*}', CmdView)
    plug.router.add_view(r'/{project}/{application}/basic', BasicListView)
    plug.router.add_view(r'/{project}/{application}/basic/{name:\w*}', BasicView)
    plug.router.add_view('', HomeView, name='index')
    return plug


if __name__ == '__main__':
    web.run_app(get_plug())
