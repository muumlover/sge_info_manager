import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from .data.controller import PerSudo
from .handle.api import *
from .handle.view import *


async def init(app):
    app['persudo_rfq_inn'] = PerSudo('rfq', 'inn')
    # app['ec_api'] = EverPhoto(app['board_api'].request)
    # with app['board_api'].data_manager('cron_job') as cron_job:
    #     if not cron_job:
    #         cron_job.update({'hour': '21,23', 'minute': '0'})
    #     # cron_job.clear()
    #     # cron_job.update({'minute': '*/1', 'second': '0'})
    #     app['board_api'].add_cron_job(key='auto_check_in', func=auto_check_in, **cron_job)


def plug_app():
    app = web.Application()
    app['name'] = 'SGE Info'
    app['static_root_url'] = '/sge_info/static'

    module_path = os.path.dirname(os.path.abspath(__file__))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(module_path + '/template'))
    app.router.add_static('/static', module_path + '/static')

    app.middlewares.append(mid_project)

    app.router.add_view(r'/api/{project}/{application}/db/{name:\w*}', DBInfo, name='api_db')
    app.router.add_view(r'/api/{project}/{application}/cmd/{name:\w*}', CMDInfo, name='api_cmd')
    app.router.add_view(r'/api/{project}/{application}/struct/{name:\w*}', STRUCTInfo, name='api_struct')

    app.router.add_view(r'/view/{project}/{application}/db', CmdListView)
    app.router.add_view(r'/view/{project}/{application}/db/{name:\w*}', CmdView)
    app.router.add_view(r'/view/{project}/{application}/cmd', CmdListView)
    app.router.add_view(r'/view/{project}/{application}/cmd/{name:\w*}', CmdView)
    app.router.add_view(r'/view/{project}/{application}/struct', StructListView)
    app.router.add_view(r'/view/{project}/{application}/struct/{name:\w*}', StructView)

    app.router.add_view('', HomeView, name='home')
    app.router.add_view('/', HomeView)
    # app.router.add_view('/config', ConfigView, name='config')
    #
    # app.router.add_get('/add', ec_task_add, name='ec_task_add')
    # app.router.add_post('/action', ec_task_action, name='ec_task_action')
    # app.router.add_post('/smscode', ec_task_smscode, name='ec_task_smscode')
    # app.router.add_view('/task/{id}', ECView, name='ec_task_item')

    app.on_startup.append(init)
    return app


if __name__ == '__main__':
    web.run_app(plug_app())
