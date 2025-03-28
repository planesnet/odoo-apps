# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # setting line.name of purchase order line, from procurement values.
    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id, values, po)
        name = values.get('description_picking', False)
        if name:
            res['name'] = name
        return res
