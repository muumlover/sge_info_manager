#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2020/1/2 12:27
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: _plug_app
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
import inspect
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web
import pathlib


class PlugIn(web.Application):
    def __init__(self, on_startup=None):
        super().__init__()
        previous_frame = inspect.currentframe().f_back
        filename, *_ = inspect.getframeinfo(previous_frame)

        plug_id = os.path.relpath(filename, 'module').split('\\', 1)[0]
        self['plug_id'] = plug_id
        self['static_root_url'] = f'/{plug_id}/static'

        module_path = pathlib.Path(os.path.abspath(f'module\\{plug_id}'))
        static_path = module_path / 'static'
        template_path = module_path / 'template'
        if not static_path.exists:
            static_path.mkdir()
        if not template_path.exists:
            template_path.mkdir()
        aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(template_path.as_posix()))
        self.router.add_static('/static', static_path)

        if on_startup:
            self.on_startup.append(on_startup)
