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


class CmdListView(View):
    @template('cmd_list.jinja2')
    async def get(self):
        return {
            'project': self.request.match_info.get('project', ''),
            'application': self.request.match_info.get('application', ''),
        }


class CmdView(View):
    @template('cmd_show.jinja2')
    async def get(self):
        return {
            'cmd_prj': self.request.match_info.get('project', ''),
            'cmd_app': self.request.match_info.get('application', ''),
            'cmd_name': self.request.match_info.get('name', ''),
        }
