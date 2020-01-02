#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:39
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: db
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from aiohttp import web

from .base import APIView


class AppInfo(APIView):
    async def get_list(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    @APIView.list_support
    async def get(self):
        name = self.request.match_info.get('name', '')
        return web.json_response({'code': 0, 'msg': '操作成功' + name, })

    async def post(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def put(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def delete(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })
