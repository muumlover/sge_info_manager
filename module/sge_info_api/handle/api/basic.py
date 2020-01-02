#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:40
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: struct
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from aiohttp import web

from .base import APIView


class BasicInfo(APIView):
    async def get_list(self):
        page = self.request.query.get('page', '0')
        limit = self.request.query.get('limit', '0')
        field = self.request.query.get('field', '')
        order = self.request.query.get('order', '')
        start = (int(page) - 1) * int(limit)
        end = (start + int(limit)) if limit != '0' else None
        struct_all = self.request['persudo'].find_all_basic()
        if field and order:
            struct_all.sort(key=lambda item: str(item.get(field)), reverse=order == 'desc')
        ret_data = struct_all[start:end]
        return web.json_response({'code': 0, 'msg': '操作成功', 'count': len(struct_all), 'data': ret_data})

    @APIView.list_support
    async def get(self):
        name = self.request.match_info.get('name', '')
        persudo = self.request['persudo']
        basic = persudo.find_basic(name)
        if not basic:
            return web.json_response({'code': -1, 'msg': '数据不存在'})
        return web.json_response({'code': 0, 'msg': '操作成功', 'data': basic})

    async def post(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def put(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def delete(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })
