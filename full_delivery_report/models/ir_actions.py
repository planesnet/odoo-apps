# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import frozendict


class IrActions(models.Model):
    _inherit = 'ir.actions.actions'

    def _get_bindings(self, model_name):
        res = super(IrActions, self)._get_bindings(model_name)
        if 'report' in res:
            report_id = self.env['ir.model.data']._xmlid_to_res_id('full_delivery_report.action_report_delivery_material', raise_if_not_found=False)
            if report_id:
                reports = list(res['report'])
                our_report = next((r for r in reports if r.get('id') == report_id), None)
                if our_report:
                    reports.remove(our_report)
                    reports.insert(0, our_report)
                    new_res = dict(res)
                    new_res['report'] = tuple(reports)
                    return frozendict(new_res)
        return res
