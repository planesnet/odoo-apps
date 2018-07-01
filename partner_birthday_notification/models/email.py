# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models

from odoo import SUPERUSER_ID
import logging.handlers
_logger = logging.getLogger(__name__)

class PartnerBirthdayNotification(models.Model):
    _inherit = 'res.partner'


    @api.model
    def mail_reminder(self):
        Mail = self.env['mail.mail']
        today = datetime.now()
        partners = self.env['res.partner'].search([])

        mail_ids = []
        for partner in partners:
            if partner.birthdate_date:
                daymonth = datetime.strptime(partner.birthdate_date, "%Y-%m-%d")
                if today.day == daymonth.day and today.month == daymonth.month:
                    mail_id = partner.send_birthday_notification()
                    if mail_id:
                        mail_ids.append(mail_id)



        Mail.send(mail_ids)
        return

    def send_birthday_notification(self):
        if not self.email:
            return False

        _logger.debug("Birthday of %s" % self.name )

        su_id = self.env['res.partner'].browse(SUPERUSER_ID)
        template_id = self.env.ref('partner_birthday_notification.birthday_notification')

        if template_id:
            values = template_id.generate_email(self.id, fields=None)
            values['email_to'] = self.email
            values['email_from'] = su_id.email
            values['res_id'] = False
            msg_id = Mail.create(values)
            return msg_id
