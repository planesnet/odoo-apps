from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMoveReversalLink(models.TransientModel):
    _name = 'account.move.reversal.link'
    _description = 'Vincular Factura Rectificativa con Origen'

    move_id = fields.Many2one('account.move', string="Factura Rectificativa", readonly=True)
    partner_id = fields.Many2one('res.partner', related='move_id.partner_id')
    company_id = fields.Many2one('res.company', related='move_id.company_id')
    move_type = fields.Selection(related='move_id.move_type')
    
    origin_move_id = fields.Many2one(
        'account.move', 
        string="Factura de Origen", 
        required=True,
    )
    copy_lines = fields.Boolean(string="¿Copiar líneas del origen? (si no hay ninguna línea en la factura)", default=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        opposite_type = 'out_invoice' if self.move_type == 'out_refund' else 'in_invoice'
        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('move_type', '=', opposite_type),
            ('state', '=', 'posted'),
            ('company_id', '=', self.company_id.id),
            ('reversed_entry_count', '=', 0),
        ]
        return {'domain': {'origin_move_id': domain}}

    def action_link_reversal(self):
        self.ensure_one()
        if self.move_id.state != 'draft':
            raise UserError(_("La factura debe estar en borrador."))

        # 1. Preparar valores básicos
        vals = {
            'reversed_entry_id': self.origin_move_id.id,
            'invoice_origin': self.origin_move_id.name,
        }
        
        # 2. Lógica de copia de líneas (si se solicita y la factura está vacía)
        if self.copy_lines and not self.move_id.invoice_line_ids:
            new_lines = []
            for line in self.origin_move_id.invoice_line_ids:
                # Copiamos los campos esenciales de la línea
                line_vals = line.copy_data({
                    'move_id': self.move_id.id,
                    'quantity': line.quantity, # Odoo ajusta el signo según el move_type
                })[0]
                new_lines.append((0, 0, line_vals))
            vals['invoice_line_ids'] = new_lines

        self.move_id.write(vals)
        
        # Log en el chatter
        self.move_id.message_post(body=_("Vinculada manualmente a la factura origen: %s") % self.origin_move_id.name)
        
        return {'type': 'ir.actions.act_window_close'}