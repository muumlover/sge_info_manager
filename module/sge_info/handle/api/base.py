#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:38
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: base
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from types import FunctionType
from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.abc import Request, StreamResponse
from aiohttp.web_middlewares import middleware
from aiohttp.web_urldispatcher import View


@middleware
async def mid_project(request: Request, handler: Callable[[Request], Awaitable[StreamResponse]]) -> StreamResponse:
    if request.rel_url.parts[2] == 'api':
        persudo_name = 'persudo_{project}_{application}'.format(
            project=request.match_info.get('project', ''),
            application=request.match_info.get('application', ''),
        )
        if persudo_name not in request.app:
            return web.json_response({'code': -1, 'msg': '操作失败，项目未找到'})
        request['persudo'] = request.app['persudo_rfq_inn']
    resp = await handler(request)
    return resp


class APIView(View):
    def list_support(func: FunctionType):
        async def ware(self, *args, **kwargs):  # self,接收body里的self,也就是类实例
            name = self.request.match_info.get('name', '')
            if not name:
                return await self.get_list()
            return await func(self, *args, **kwargs)

        return ware

    async def get_list(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    @list_support
    async def get(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def post(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def put(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def delete(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })
