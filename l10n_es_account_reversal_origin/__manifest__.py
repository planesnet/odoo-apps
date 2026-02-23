{
    'name': 'Spain - Account Reversal Origin Link',
    'version': '18.0.1.1.0',
    'summary':  """
        Vincular facturas rectificativas manuales con su origen y copiar líneas, si 
        la rectificativa no tiene líneas, se traiga las de la factura original con signo invertido. 
    """,
    'category': 'Accounting/Localizations',
    'author': 'Planesnet Informática',
    'website': 'https://www.planesnet.com',
    'depends': ['account', 'l10n_es'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_move_reversal_link_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}