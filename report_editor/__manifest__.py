# -*- coding: utf-8 -*-
{
    'name': "Editor de reportes Odoo 19",
    'version': '19.0.2.0.0',
    'author': "Planes Soluciones Informáticas",
    'category': 'Web',
    'depends': ['base', 'web', 'html_editor', 'account'],
    'data': [
        'views/res_company_views.xml',
        'views/report_actions.xml',
        'views/invoice_toggle.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'report_editor/static/src/js/wysiwyg.js'
        ],
    },
    'installable': True,
    'license': 'OPL-1',
}