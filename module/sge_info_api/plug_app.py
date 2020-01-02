import pathlib

from aiohttp import web

from ac_api import PlugIn
from .data.controller import PerSudo
from .handle.api import *


async def init(plug):
    plug['persudo'] = {}
    persudo_dir = pathlib.Path(__file__).with_name('data') / 'persudo'
    for persudo in persudo_dir.glob('*/*'):
        if not (persudo / 'input').exists():
            continue
        persudo_prj = persudo.parent.name
        persudo_app = persudo.name
        plug['persudo'][f'{persudo_prj}_{persudo_app}'] = PerSudo(persudo_prj, persudo_app)


def get_plug():
    plug = PlugIn(on_startup=init)
    plug.middlewares.append(mid_project)
    plug.router.add_view(r'', ProjectInfo)
    plug.router.add_view(r'/{project}/{application}', AppInfo)
    plug.router.add_view(r'/{project}/{application}/db/{name:\w*}', DBInfo)
    plug.router.add_view(r'/{project}/{application}/cmd/{name:\w*}', CMDInfo)
    plug.router.add_view(r'/{project}/{application}/basic/{name:\w*}', BasicInfo)
    return plug


if __name__ == '__main__':
    web.run_app(get_plug())
