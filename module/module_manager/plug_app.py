#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/5 13:50 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : auto_command
@FileName: module_manager
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""

from aiohttp import web

from ac_api import PlugIn
from .handle.handle_config import ConfigView


async def init(plug):
    pass


def get_plug():
    plug = PlugIn(on_startup=init)
    plug.router.add_view('/config', ConfigView, name='config')
    return plug


if __name__ == '__main__':
    web.run_app(get_plug())
