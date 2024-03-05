# __manifest__.py

{
    'name': 'Dispatch Management System',
    'version': '1.0',
    'category': 'Uncategorized',
    'license': "LGPL-3",
    'author': 'Yagnik (yagp)',
    'summary': 'Install Stock Transport',
    'depends': ['stock'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
