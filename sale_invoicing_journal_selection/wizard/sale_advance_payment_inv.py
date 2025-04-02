# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    journal_id = fields.Many2one('account.journal', string='Journal', ondelete='cascade', domain="[('type', '=', 'sale')]", check_company=True)

    def _create_invoices(self, sale_orders):
        if self.advance_payment_method == "delivered" and self.journal_id:
            ctx = self.env.context.copy()
            ctx.update(
                {
                    "default_journal_id": self.journal_id.id,
                }
            )
            return sale_orders.with_context(**ctx)._create_invoices(
                final=self.deduct_down_payments, grouped=not self.consolidated_billing
            )
        invoices = super()._create_invoices(sale_orders)


        # prioritt over other modules
        if self.journal_id:
            for invoice in invoices:
                if invoice.journal_id != self.journal_id:
                    invoice.journal_id = self.journal_id
            return invoices
        


    def _prepare_invoice_values(self, order, so_line):
        res = super()._prepare_invoice_values(order, so_line)
        if self.journal_id:
            res["journal_id"] = self.journal_id.id
        return res

