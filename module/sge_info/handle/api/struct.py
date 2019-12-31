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


class STRUCTInfo(APIView):
    async def get_list(self):
        page = self.request.query.get('page', '0')
        limit = self.request.query.get('limit', '0')
        field = self.request.query.get('field', '')
        order = self.request.query.get('order', '')
        start = (int(page) - 1) * int(limit)
        end = (start + int(limit)) if limit != '0' else None

        struct_all = [{**{
            '_id': struct['type'],
            'name': struct['name'],
            'base64': struct['base64'],
            'enable': struct['enable'],
            'gtpno': struct.get('gtpno', ''),
            'db_name': struct['db_name'],
            'db_type': struct['db_type'],
            'times': struct['times'],
        }, **dict(zip(
            ['group', 'type', 'length'],
            self.request['persudo'].struct_type(struct['type'])
        ))} for struct in self.request['persudo'].struct_find_all()]

        if field and order:
            struct_all.sort(key=lambda item: str(item.get(field)), reverse=order == 'desc')

        ret_data = struct_all[start:end]
        return web.json_response({'code': 0, 'msg': '操作成功', 'count': len(struct_all), 'data': ret_data})

    @APIView.list_support
    async def get(self):
        name = self.request.match_info.get('name', '')
        persudo = self.request['persudo']
        struct = persudo.struct_find(name)
        if not struct:
            return web.json_response({'code': -1, 'msg': '数据不存在'})
        ret_data = {**{
            '_id': struct['type'],
            'name': struct['name'],
            'base64': struct['base64'],
            'enable': struct['enable'],
            'gtpno': struct.get('gtpno', ''),
            'db_name': struct['db_name'],
            'db_type': struct['db_type'],
            'times': struct['times'],
            # 'struct': [struct['struct']],
            'fields': [{
                'f_name': fields['name'],
                'f_type': {**{
                    't_id': persudo.struct_id(fields['type']),
                    't_name': persudo.struct_name(fields['type']),
                }, **dict(zip(
                    ['t_group', 't_type', 't_length'],
                    persudo.struct_type(fields['type'])
                ))}
            } for fields in struct['struct']['sub']] if struct['struct'] and 'sub' in struct['struct'] else None,
        }, **dict(zip(
            ['group', 'type', 'length'],
            self.request['persudo'].struct_type(struct['type'])
        ))}
        return web.json_response({'code': 0, 'msg': '操作成功', 'data': ret_data})

    async def post(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def put(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })

    async def delete(self):
        return web.json_response({'code': 0, 'msg': '操作成功', })
