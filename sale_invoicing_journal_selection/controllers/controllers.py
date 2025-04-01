# -*- coding: utf-8 -*-
# from odoo import http


# class StockPickingDescription(http.Controller):
#     @http.route('/stock_picking_description/stock_picking_description', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_description/stock_picking_description/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_description.listing', {
#             'root': '/stock_picking_description/stock_picking_description',
#             'objects': http.request.env['stock_picking_description.stock_picking_description'].search([]),
#         })

#     @http.route('/stock_picking_description/stock_picking_description/objects/<model("stock_picking_description.stock_picking_description"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_description.object', {
#             'object': obj
#         })

