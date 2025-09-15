# -*- coding: utf-8 -*-
{
    'name': "partner_pricelist_report",

    'summary': "Print partner pricelist report",

    'description': """
Print partner pricelist report
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '3.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/partner_pricelist_report.xml',
        'report/ir_actions_report.xml',
        
        'views/views.xml',
        'views/templates.xml',
    ],
}

