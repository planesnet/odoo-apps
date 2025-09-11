# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


# class PartnerPricelistReport(models.AbstractModel):
#     _name = 'report.partner.report_pricelist'
#     _description = 'Partner Pricelist Report'

#     def _get_report_values(self, docids, data):
#         return self._get_report_data(data, 'pdf')

#     @api.model
#     def get_html(self, data):
#         render_values = self._get_report_data(data, 'html')
#         return self.env['ir.qweb']._render('partner_pricelist_report.report_pricelist_page', render_values)

#     def _get_report_data(self, data, report_type='html'):
#         active_ids = data.get('active_ids') or []

#         partners = self.env['res.partner'].browse(active_ids)
#         partners_data = [self._get_partner_data(partner) for partner in partners]

#         return {
#             'is_html_type': report_type == 'html',
#             'display_pricelist_title': data.get('display_pricelist_title', False) and bool(data['display_pricelist_title']),
#             'partners': partners_data,
#         }

#     def _get_partner_data(self, partner):
#         data = {
#             'id': partner.id,
#             'name': partner.name,
#             'pricelist': partner.property_product_pricelist,
#         }


#         return data
