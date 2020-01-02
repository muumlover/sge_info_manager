#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/30 13:48
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : sge_info_manager
@FileName: controller
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
import json
import os
import pathlib


class Catalogue:
    def __init__(self, dir_path):
        self._catalogue = {}
        self.dir_path = dir_path
        for file_name in os.listdir(self.dir_path):
            catalogue = {'index': list(), 'value': list()}
            with open(self.dir_path / file_name) as fp:
                const_list = json.load(fp)
                if not isinstance(const_list, list):
                    continue
                for const in const_list:
                    if 'const' in file_name:
                        catalogue['index'].append(const['name'])
                    else:
                        catalogue['index'].append(const['type'])
                    catalogue['value'].append(const)
            self._catalogue[file_name] = catalogue

    def read_cataloguee(self, filename, index_name):
        if filename not in self._catalogue:
            return {}
        if index_name not in self._catalogue[filename]['index']:
            return {}
        idx = self._catalogue[filename]['index'].index(index_name)
        return self._catalogue[filename]['value'][idx]

    def basic(self, type_):
        return self.read_cataloguee('basic.py', type_)

    def basic_list(self):
        return self.read_all_cataloguee('basic.py')

    def tbl_const(self, name_):
        return self.read_cataloguee('tblconst.py', name_)

    def tbl_struct(self, type_):
        return self.read_cataloguee('tblstruct.py', type_)

    def fld_struct(self, type_):
        return self.read_cataloguee('fldstruct.py', type_)

    def cmd_const(self, name_):
        return self.read_cataloguee('cmdconst.py', name_)

    def cmd_struct(self, type_):
        return self.read_cataloguee('cmdstruct.py', type_)

    def read_all_cataloguee(self, filename):
        if filename not in self._catalogue:
            return {}
        return self._catalogue[filename]['value']

    def cmd_const_list(self):
        return self.read_all_cataloguee('cmdconst.py')

    def find_all_tbl_const(self):
        return self.read_all_cataloguee('tblconst.py')


class PerSudo:
    project = ''
    application = ''

    def __init__(self, project, application):
        self.project = project
        self.application = application
        self.data = Catalogue(self._file_path)
        pass

    @property
    def _file_path(self):
        data_dir = pathlib.Path(__file__).parent
        input_dir = data_dir / 'persudo' / self.project / self.application / 'input'
        return input_dir

    def reload(self):
        self.data = Catalogue(self._file_path)

    def _basic_mem(self, basic, cmd_name=None):
        if 'mem' not in basic:
            return ['MISS MEM'] * 5
        t_group, t_type, t_length, t_link, t_fields = '', '', None, False, None
        for k, v in basic['mem'].items():
            if k in ['char', 'buf']:
                t_group, t_type, t_length = 'BASE', k, v['length']
            elif k in ['long long', 'double']:
                t_group, t_type = 'BASE', k
            elif k == 'other':
                struct = None
                t_group, t_type = 'GROUP MISS', v['name']
                if v['name'][:3] == 'tbl':
                    struct = self.data.tbl_struct(basic['type'])
                    t_group, t_link = 'TBL', bool(struct)
                elif v['name'][:3] == 'fld':
                    struct = self.data.fld_struct(basic['type'])
                    t_group, t_link = 'FLD', bool(struct)
                if struct:
                    t_fields = [self._field_format(field, cmd_name) for field in struct['sub']]
            else:
                t_type = 'MISS TYPE'
            break
        return t_group, t_type, t_length, t_link, t_fields

    def _basic_gtp(self, basic, cmd_name):
        if 'gtp' not in basic:
            return ['MISS GTP'] * 4
        if cmd_name not in basic['gtp']:
            return ['MISS CMD'] * 4
        gtp = basic['gtp'][cmd_name]
        gtp_num = gtp.get('fieldnum')
        gtp_desc = gtp.get('fielddesc')
        gtp_mem = gtp.get('fieldmem')
        gtp_name = gtp.get('fieldname')
        return gtp_num, gtp_desc, gtp_mem, gtp_name

    def _command_format(self, command):
        if 'ch_name' in command:
            return {
                'name': command.get('name'),
                'type': command.get('type'),
                'cmdno': command.get('cmdno'),
                'cmdtype': command.get('gtp'),
                'cmdname': command.get('ch_name'),
            }
        return {
            'name': command.get('name'),
            'type': command.get('type'),
            'cmdno': command.get('cmdno'),
            'cmdtype': command.get('cmdtype'),
            'cmdname': command.get('cmdname'),
        }

    def _basic_format(self, basic, cmd_name=None):
        return {**{
            'type': basic.get('type'),
            'gtp': bool(basic.get('gtp')),
            'dbinfo': bool(basic.get('dbinfo')),
        }, **dict(zip(
            ['t_group', 't_type', 't_length', 't_link'],
            self._basic_mem(basic, cmd_name)
        ))}

    def _field_format(self, field, cmd_name=None):
        basic = self.data.basic(field.get('type'))
        return {**{
            'f_name': field.get('name'),
        }, **dict(zip(
            ['t_group', 't_type', 't_length', 't_link', 't_fields'],
            self._basic_mem(basic, cmd_name)
        )), **dict(zip(
            ['gtp_num', 'gtp_desc', 'gtp_mem', 'gtp_name'],
            self._basic_gtp(basic, cmd_name)
        ) if cmd_name and basic.get('gtp') and basic.get('gtp').get(cmd_name) else {})}

    def find_cmd(self, name):
        cmd_const = self.data.cmd_const(name)
        if not cmd_const:
            return {}, {}
        cmd_out = self._command_format(cmd_const)
        cmd_out['fields'] = None
        struct = self.data.cmd_struct(cmd_const['name'])
        if struct:
            cmd_out['fields'] = [self._field_format(field, cmd_name=name) for field in struct['sub']]
        return cmd_out

    def find_basic(self, name):
        basic = self.data.basic(name)
        if not basic:
            return {}
        basic_out = self._basic_format(basic)
        basic_out['fields'] = None
        struct = None
        for k, v in basic['mem'].items():
            if k in ['char', 'buf', 'long long', 'double']:
                break
            if k == 'other':
                if v['name'][:3] == 'tbl':
                    struct = self.data.tbl_struct(name)
                elif v['name'][:3] == 'fld':
                    struct = self.data.fld_struct(name)
                break
        if struct:
            basic_out['fields'] = [self._field_format(field) for field in struct['sub']]
        return basic_out

    def find_all_cmd(self):
        return [self._command_format(basic) for basic in self.data.cmd_const_list()]

    def find_all_basic(self):
        return [self._basic_format(basic) for basic in self.data.basic_list()]

    def _struct_find_all_type_1(self):
        return [{**{
            '_id': basic.get('type'),
            'name': basic.get('name'),
            'ch_name': basic.get('ch_name'),
            'base64': basic.get('base64'),
            'enable': basic.get('enable'),
            'gtpno': basic.get('gtpno', ''),
            'db_name': basic.get('db_name'),
            'db_type': basic.get('db_type'),
            'times': basic.get('times'),
        }, **dict(zip(
            ['group', 'type', 'length'],
            self._basic_mem(basic)
        ))} for basic in self.data.basic_list()]

    def struct_id(self, name):
        struct = self.data.basic(name)
        if 'type' not in struct:
            return 'MISS TYPE'
        return struct['type']

    def struct_name(self, name):
        struct = self.data.basic(name)
        if 'name' not in struct:
            return 'MISS NAME'
        return struct['name']


if __name__ == '__main__':
    ctrl = PerSudo('rfq', 'inn')
    a = ctrl.find_cmd('rfq_inst_info_nty')
    pass
