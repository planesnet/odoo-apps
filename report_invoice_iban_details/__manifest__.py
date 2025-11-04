# -*- coding: utf-8 -*-
{
    'name': 'Mostrar IBAN en Factura de venta',
    'version': '19.0.1.0.1',
    'summary': 'Añade el primer IBAN (saneado) del cliente en el informe de factura.',
    'description': """
        Este módulo personaliza el informe de factura (account.report_invoice_document)
        para mostrar el primer número de cuenta con parte oculta (ej. ES12341234********12) 
        que se encuentre en la ficha del cliente, sólo si la condición de pago seleccionada 
        es 'Recibo bancario'.
        
        NO depende de los mandatos SEPA.
    """,
    'author': "Planes Soluciones Informáticas",
    'website': "https://www.planesnet.com",
    'category': 'Accounting/Localisation',
    'license': 'AGPL-3',
            
    'depends': [
        'account',
    ],    
    
    'data': [
        'views/report_invoice_templates.xml',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}