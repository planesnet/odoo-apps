{
    'name': 'report_receipt_totals',
    'version': '18.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Ticket de cierre de sesión en formato 80mm',
    'author': 'Planes',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'point_of_sale',
        'web',
    ],
    'data': [
        'report/report_receipt.xml',
    ],
    'installable': True,
    'application': False,
}