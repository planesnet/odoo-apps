# -*- coding: utf-8 -*-
{
    'name': "zebra_printer_connector",

    'summary': "Módulo para lanzar la impresión en la Zebra desde Odoo mediante el WebSocketServer",

    'description': """
Long description of module's purpose
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.3.0',

    # any module necessary for this one to work correctly
    'depends': ['base','zebra_printer'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'zebra_printer_connector/static/src/js/zebra_printer_connector.js',
            'zebra_printer_connector/static/src/xml/templates.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'OEEL-1',

}

