# -*- coding: utf-8 -*-
{
    'name': "product_full_pricelist",
    'summary': "Show full information on product price list report",

    'description': """
Full product price list report.
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base','web','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/product_pricelist_report.xml',
    ],
    'assets': {
        'web.assets_backend': [  
        ],
    },

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",
    'support': "info@planesnet.com",
    'license': 'OPL-1',


    # Odoo store
    #'images': ['static/description/banner.jpg'],    
    'price': 50.0,
    'currency': 'EUR',
}

