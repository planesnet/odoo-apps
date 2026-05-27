# -*- coding: utf-8 -*-
import os

report_ref = 'full_delivery_report.full_delivery_report'
report = self.env['ir.actions.report']._get_report_from_name(report_ref)
pdf_content, _ = report._render_qweb_pdf(report_ref, res_ids=[1])

output_path = '/home/luis/cowork/odoo-apps/custom/full_delivery_report/scratch/picking_1.pdf'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'wb') as f:
    f.write(pdf_content)

print(f"PDF successfully written to: {output_path}")

try:
    import fitz
    doc = fitz.open(output_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    image_path = '/home/luis/cowork/odoo-apps/custom/full_delivery_report/scratch/picking_1.png'
    pix.save(image_path)
    print(f"PNG successfully written to: {image_path}")
except Exception as e:
    print(f"Could not convert PDF to PNG: {e}")
