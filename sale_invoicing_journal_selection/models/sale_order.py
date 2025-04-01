# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        values = super()._prepare_invoice()
        if "default_journal_id" in self.env.context:
            values.update(
                {
                    "journal_id": self.env.context["default_journal_id"],
                }
            )
        return values