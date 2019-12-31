#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:59
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: struct
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template


class StructListView(View):
    @template('struct_list.jinja2')
    async def get(self):
        return {
            'project': self.request.match_info.get('project', ''),
            'application': self.request.match_info.get('application', ''),
        }


class StructView(View):
    @template('struct_list.jinja2')
    async def get(self):
        return {
            'project': self.request.match_info.get('project', ''),
            'application': self.request.match_info.get('application', ''),
        }
