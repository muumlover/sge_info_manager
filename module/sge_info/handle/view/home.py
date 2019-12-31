#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 17:59
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: home
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template


class HomeView(View):
    @template('home.jinja2')
    async def get(self):
        board = self.request.app['board']
        plug_list = []
        for module in board.module_all.values():
            if module.name == 'module_manager':
                continue
            plug_list.append(module)
        return {'plug_list': plug_list}
