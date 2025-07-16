# -*- coding: utf-8 -*-
from odoo import http

# class ZebraPrinter(http.Controller):
#     @http.route('/zebra_printer/zebra_printer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zebra_printer/zebra_printer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zebra_printer.listing', {
#             'root': '/zebra_printer/zebra_printer',
#             'objects': http.request.env['zebra_printer.zebra_printer'].search([]),
#         })

#     @http.route('/zebra_printer/zebra_printer/objects/<model("zebra_printer.zebra_printer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zebra_printer.object', {
#             'object': obj
#         })