# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestDeliveryReport(TransactionCase):

    def setUp(self):
        super(TestDeliveryReport, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Material',
            'type': 'consu',
        })
        self.picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        self.location_stock = self.env.ref('stock.stock_location_stock')
        self.location_customer = self.env.ref('stock.stock_location_customers')

        self.picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type.id,
            'location_id': self.location_stock.id,
            'location_dest_id': self.location_customer.id,
        })

        self.env['stock.move'].create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 10.0,
            'quantity': 10.0,
            'product_uom': self.product.uom_id.id,
            'picking_id': self.picking.id,
            'location_id': self.location_stock.id,
            'location_dest_id': self.location_customer.id,
        })

    def test_full_delivery_report_pdf(self):
        """Test the generation of the Delivery Report PDF."""
        report_ref = 'full_delivery_report.full_delivery_report'
        report = self.env['ir.actions.report']._get_report_from_name(report_ref)
        pdf_content, _ = report._render_qweb_pdf(report_ref, res_ids=self.picking.ids)
        self.assertTrue(pdf_content, "The generated PDF should not be empty")

    def test_report_binding_order(self):
        """Test that our report is placed first in the bindings."""
        bindings = self.env['ir.actions.actions'].get_bindings('stock.picking')
        self.assertIn('report', bindings)
        reports = bindings['report']
        self.assertTrue(reports)
        # The first report in the bindings should be ours
        report_id = self.env.ref('full_delivery_report.action_report_delivery_material').id
        self.assertEqual(reports[0]['id'], report_id, "Our report should be at the very top of the reports list")
