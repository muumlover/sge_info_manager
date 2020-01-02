#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:39
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: cmd
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from aiohttp import web

from .base import APIView


class CMDInfo(APIView):
    async def get_list(self):
        page = self.request.query.get('page', '0')
        limit = self.request.query.get('limit', '0')
        field = self.request.query.get('field', '')
        order = self.request.query.get('order', '')
        start = (int(page) - 1) * int(limit)
        end = start + int(limit) if limit != '0' else None

        cmd_all = self.request['persudo'].find_all_cmd()

        if field and order:
            cmd_all.sort(key=lambda item: item.get(field), reverse=order == 'desc')

        ret_data = cmd_all[start:end]
        return web.json_response({'code': 0, 'msg': '操作成功', 'count': len(cmd_all), 'data': ret_data})

    @APIView.list_support
    async def get(self):
        name = self.request.match_info.get('name', '')
        persudo = self.request['persudo']
        cmd_info = persudo.find_cmd(name)
        if not cmd_info:
            return web.json_response({'code': -1, 'msg': '数据不存在'})
        # ret_data = {
        #     '_id': cmd_const['type'],
        #     'name': cmd_const['name'],
        #     'cmdno': cmd_const['cmdno'],
        #     'ch_name': cmd_const['ch_name'],
        #     'gtp': cmd_const['gtp'],
        #     'fields': [{
        #         'f_name': fields['name'],
        #         'f_type': {**{
        #             't_id': persudo.struct_id(fields['type']),
        #             't_name': persudo.struct_name(fields['type']),
        #         }, **dict(zip(
        #             ['t_group', 't_type', 't_length'],
        #             persudo.struct_mem(fields['type'])
        #         ))}
        #     } for fields in cmd_struct['sub']]
        # }
        return web.json_response({'code': 0, 'msg': '操作成功', 'data': cmd_info})

    async def post(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def put(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def delete(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })
