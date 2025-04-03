# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com

from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # setting line.description_picking of drop shipping lines, from purchase order lines.
    def _prepare_stock_moves(self, picking):
        res = super()._prepare_stock_moves(picking)
        for re in res:
            re['description_picking'] = self.name
        return res    