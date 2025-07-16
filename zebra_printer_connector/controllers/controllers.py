# -*- coding: utf-8 -*-
# from odoo import http


# class ZebraPrinterConnector(http.Controller):
#     @http.route('/zebra_printer_connector/zebra_printer_connector', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zebra_printer_connector/zebra_printer_connector/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zebra_printer_connector.listing', {
#             'root': '/zebra_printer_connector/zebra_printer_connector',
#             'objects': http.request.env['zebra_printer_connector.zebra_printer_connector'].search([]),
#         })

#     @http.route('/zebra_printer_connector/zebra_printer_connector/objects/<model("zebra_printer_connector.zebra_printer_connector"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zebra_printer_connector.object', {
#             'object': obj
#         })

