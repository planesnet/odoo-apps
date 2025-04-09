# -*- coding: utf-8 -*-
# from odoo import http


# class ProductFullPricelist(http.Controller):
#     @http.route('/product_full_pricelist/product_full_pricelist', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_full_pricelist/product_full_pricelist/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_full_pricelist.listing', {
#             'root': '/product_full_pricelist/product_full_pricelist',
#             'objects': http.request.env['product_full_pricelist.product_full_pricelist'].search([]),
#         })

#     @http.route('/product_full_pricelist/product_full_pricelist/objects/<model("product_full_pricelist.product_full_pricelist"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_full_pricelist.object', {
#             'object': obj
#         })

