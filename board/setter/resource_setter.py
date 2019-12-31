#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/15 10:54 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCheckIn
@FileName: resource_setter
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import os
import pathlib
import aiohttp_jinja2
import jinja2


def resource_set(app):
    base_path = pathlib.Path.cwd() / 'board'
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(base_path / 'template')))
    app.router.add_static('/static', base_path / 'static')
