# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com

from odoo import fields, models
class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    journal_id = fields.Many2one('account.journal', string='Journal', ondelete='cascade', domain="[('type', '=', 'sale')]", check_company=True)



    def _create_invoices(self, sale_orders):
        invoices = super()._create_invoices(sale_orders)

        # priority over other modules
        if self.journal_id:
            invoices.write({'journal_id': self.journal_id.id})

        return invoices
        
