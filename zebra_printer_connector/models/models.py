# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardSelectPrinter(models.Model):
    _name = "wizard.select.printer"
    _description = "Modelo para representar el wizard de selección de impresora"

    @api.model
    def printer_default(self):
        user_id =  self.env.user
        if user_id.printer_id:
            return user_id.printer_id.id

    printer_id = fields.Many2one("zebra.printer", string="Impresora", required=True, default=printer_default)
    active_id = fields.Integer("ActiveId")
    model_name = fields.Char("Model name")
    report_name = fields.Char("Report name")
    printer_ip = fields.Char("Printer IP", compute="_compute_printer_ip", store=True)

    @api.depends('printer_id','printer_id.ip')
    def _compute_printer_ip(self):
        for record in self:
            if record.printer_id:
                record.printer_ip = record.printer_id.ip
            else:
                record.printer_ip = "0.0.0.0"

    def print_zebra_printer_label(self):
        self.ensure_one()

        action = self.env["ir.actions.client"]._for_xml_id("zebra_printer_connector.accion_imprimir_etiqueta")
        action['context'] = {'active_id': self.active_id, 'model_name': self.model_name, 'report_name': self.report_name, 'printer_ip': self.printer_ip}
        return action
