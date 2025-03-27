# -*- coding: utf-8 -*-
{
    'name': "stock_picking_description",

    'summary': "Copia la descripción de las líneas de venta en la descripción de los movimientos de stock.",

    'description': """
Copia la descripción de las líneas de venta en la descripción de los movimientos de stock.
Pedido de venta -> Documento de entrega.
Pedido de venta -> Picking o documento de elección de productos.
Pedido de venta -> Compra (cuando se activa la ruta Drop shipping).
Pedido de compra -> Documento de salida
    """,

    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

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
}

