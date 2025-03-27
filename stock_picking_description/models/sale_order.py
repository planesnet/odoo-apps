# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['description_picking']
        return fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'description_picking': self.name,
        })
        return values

