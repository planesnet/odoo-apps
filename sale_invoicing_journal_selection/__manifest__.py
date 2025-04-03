# -*- coding: utf-8 -*-
{
    'name': "Sale Invoicing Journal Selection",

    'summary': "Select the journal when you create invoices",

    'description': """
Select the accounting journal to use when invoicing pending orders. 
When you invoice pending orders en masse and want to record the generated invoice entries in a specific accounting journal, it's most practical to indicate this at the time the invoices are created.
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",
    'support': "info@planesnet.com",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting & Finance',
    'version': '1.0.2',
    'license': 'OPL-1',
    

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],



    # Odoo store
    'images': ['static/description/banner.jpg'],    
    'price': 25.0,
    'currency': 'EUR',
}

