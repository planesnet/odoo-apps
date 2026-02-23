from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Aplicamos el contexto para que el creador (uid) no sea seguidor automático
        records = super(AccountMove, self.with_context(mail_create_nosubscribe=True)).create(vals_list)
        
        # 2. Si quieres eliminar al comercial (user_id) específicamente:
        for record in records:
            if record.user_id:
                # Obtenemos el partner_id del usuario comercial
                commercial_partner = record.user_id.partner_id
                # Desuscribimos al comercial
                record.message_unsubscribe(partner_ids=commercial_partner.ids)
                
        return records