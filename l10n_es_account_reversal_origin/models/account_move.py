# -*- coding: utf-8 -*-
from odoo import models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_reversal_link_wizard(self):
        self.ensure_one()
        return {
            'name': _('Vincular Factura de Origen'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.reversal.link',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
            },
        }