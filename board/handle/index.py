import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class IndexView(View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        sub_index, sub_config = [], []
        for module in self.request.app.module_all.values():
            if not module.loaded:
                continue
            if module.app.router.get('index'):
                sub_index.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'],
                    'link': module.app.router.get('index').url_for(),
                })
            if module.app.router.get('config'):
                sub_config.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'] + '设置',
                    'link': module.app.router.get('config').url_for(),
                })

        sub_index += [
            {
                'icon': '',
                'title': '周报系统',
                'link': 'http://mars.sge-tech.com/',
            },
            {
                'icon': '',
                'title': '开发管理平台',
                'link': 'http://nuggets.sge-tech.com/',
            },
        ]

        return {
            'name': 'SGE CENTER',
            'main_menu': [
                {
                    'icon': '',
                    'title': '所有应用',
                    'sub_menu': sub_index + [
                        {
                            'icon': '',
                            'title': '敬请期待',
                            'link': 'error',
                        }
                    ]
                },
                {
                    'icon': '',
                    'title': '应用设置',
                    'sub_menu': sub_config + [

                    ]
                }
            ]
        }
