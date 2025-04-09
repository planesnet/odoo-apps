# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class ProductPricelistReport(models.AbstractModel):
    _inherit = 'report.product.report_pricelist'
    _description = 'Pricelist Report'

    def _get_product_data(self, is_product_tmpl, product, pricelist, quantities):
        data = super()._get_product_data(is_product_tmpl, product, pricelist, quantities)
        if is_product_tmpl:
            data['list_price'] = product.list_price

        else:    
            data['list_price'] = product.lst_price

        return data
