# -*- coding: utf-8 -*-
{
    'name': "Stock picking description",

    'summary': "Copy the description of the sales lines into the description of the stock movements.",

    'description': """
For each sales or purchase order line, if the order line description has been edited, it is propagated to the stock movements generated. The documents to which this propagation occurs are the stock delivery and receipt documents, as well as the "drop shipping" movement.
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",
    'support': "info@planesnet.com",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '1.1.1',
    'license': 'OPL-1',
    

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale','purchase','stock_dropshipping'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],



    # Odoo store
    'images': ['static/description/banner.jpg'],    
    'price': 25.0,
    'currency': 'EUR',
}

