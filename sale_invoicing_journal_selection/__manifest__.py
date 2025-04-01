# -*- coding: utf-8 -*-
{
    'name': "Sale Invoicing Journal Selection",

    'summary': "Select the journal when you create invoices",

    'description': """
Select the journal when you create invoices.
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",
    'support': "info@planesnet.com",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '1.0',
    'license': 'AGPL-3',
    

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/views.xml',
    ],



    # Odoo store
    'images': ['static/description/banner.jpg'],    
    'price': 0.0,
    'currency': 'EUR',
}

