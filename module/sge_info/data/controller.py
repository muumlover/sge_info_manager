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


class Catalogue:
    def __init__(self, dir_path):
        self._catalogue = {}
        self.dir_path = dir_path
        for file_name in os.listdir(self.dir_path):
            catalogue = {'index': list(), 'value': list()}
            with open(self.dir_path + file_name) as fp:
                const_list = json.load(fp)
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

    def find_basic(self, type_):
        return self.read_cataloguee('basic.py', type_)

    def find_tbl_const(self, name_):
        return self.read_cataloguee('tblconst.py', name_)

    def find_tbl_struct(self, type_):
        return self.read_cataloguee('tblstruct.py', type_)

    def find_fld_struct(self, type_):
        return self.read_cataloguee('fldstruct.py', type_)

    def find_cmd_const(self, name_):
        return self.read_cataloguee('cmdconst.py', name_)

    def find_cmd_struct(self, type_):
        return self.read_cataloguee('cmdstruct.py', type_)

    def read_all_cataloguee(self, filename):
        if filename not in self._catalogue:
            return {}
        return self._catalogue[filename]['value']

    def find_all_basic(self):
        return self.read_all_cataloguee('basic.py')

    def find_all_cmd_const(self):
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
        return '{base}/persudo/{project}/{application}/input/'.format(
            base=os.path.split(__file__)[0],
            project=self.project,
            application=self.application
        )

    def reload(self):
        self.data = Catalogue(self._file_path)

    def cmd_find_all(self):
        return self.data.find_all_cmd_const()

    def struct_find_all(self):
        return self.data.find_all_basic()

    def cmd_find(self, name):
        cmd_const = self.data.find_cmd_const(name)
        if not cmd_const:
            return {}, {}
        cmd_struct = self.data.find_cmd_struct(cmd_const['type'])
        return cmd_const, cmd_struct

    def struct_find(self, name):
        struct = self.data.find_basic(name)
        if not struct:
            return {}
        struct['struct'] = None
        for k, v in struct['mem'].items():
            if k in ['char', 'buf']:
                # return k, v['length']
                return struct
            if k in ['long long', 'double']:
                # return k
                return struct
            if k == 'other':
                if v['name'][:3] == 'tbl':
                    struct['struct'] = self.data.find_tbl_struct(name)
                elif v['name'][:3] == 'fld':
                    struct['struct'] = self.data.find_fld_struct(name)
                return struct
        return {}

    def struct_id(self, name):
        struct = self.data.find_basic(name)
        if 'type' not in struct:
            return 'MISS TYPE'
        return struct['type']

    def struct_name(self, name):
        struct = self.data.find_basic(name)
        if 'name' not in struct:
            return 'MISS NAME'
        return struct['name']

    def struct_type(self, name):
        struct = self.data.find_basic(name)
        if 'mem' not in struct:
            return 'MISS MEM', 'MISS MEM', 'MISS MEM'
        for k, v in struct['mem'].items():
            if k in ['char', 'buf']:
                return 'BASE', k, v['length']
            if k in ['long long', 'double']:
                return 'BASE', k, None
            if k == 'other':
                if v['name'][:3] == 'tbl':
                    if self.data.find_tbl_struct(name):
                        return 'TBL', v['name'], None
                    else:
                        return 'MISS TBL', v['name'], None
                elif v['name'][:3] == 'fld':
                    if self.data.find_fld_struct(name):
                        return 'FLD', v['name'], None
                    else:
                        return 'MISS FLD', v['name'], None
                return 'GROUP MISS', v['name'], None
        return 'MISS GROUP', 'MISS TYPE', 'MISS LEN'


if __name__ == '__main__':
    ctrl = PerSudo('rfq', 'inn')
    a = ctrl.cmd_find('rfq_inst_info_nty')
    pass
