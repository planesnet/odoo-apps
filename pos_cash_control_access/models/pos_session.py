from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def try_cash_in_out(self, income, amount, reason, extras=None):
        """
        Elevamos privilegios a superusuario para permitir que cajeros
        registren movimientos de caja sin necesidad de permisos en account.move
        """
        return super(PosSession, self.sudo()).try_cash_in_out(income, amount, reason, extras)