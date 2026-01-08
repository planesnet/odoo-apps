# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com

from odoo import api, models

class StockRule(models.Model):
    _inherit = 'stock.rule'

    # Se utiliza para copiar la descripción de la línea de picking al siguiente movmiento de entrega.
    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        new_move_values = super()._push_prepare_move_copy_values(move_to_copy, new_date)
        new_move_values.update({
            'description_picking': move_to_copy.description_picking,
        })
        return new_move_values
