# -*- coding: utf-8 -*-
{
    'name': 'Restrict Create Partner From Documents',
    'version': '19.0.1.0.0',    
    'category': 'Customizations',
    'summary': 'Restricts creating partners from sales, purchases and invoices.',
    'author': 'Planesnet',
    'website': 'https://www.planesnet.com',
    'license': 'AGPL-3',
    'depends': [
        'sale_management',
        'purchase',
        'account',
    ],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
}