# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
import re

from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # setting line.name of purchase order line, from procurement values.
    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, company_id, values, po)
        description_picking = values.get('description_picking', False)
        if description_picking:
            name = res['name']
            if description_picking != name:
                # Se busca la referencia del proveedor en el 'name', que está entre corchetes.
                # Ejemplo: "[REF001] Producto A" -> match.group(1) será "REF001"
                match_ref = re.search(r'\[(.*?)\]', name)
                
                # Se busca la descripción del producto en 'description_picking', que está después de los corchetes.
                # Ejemplo: "[OTRA_REF] Producto A con color especial" -> match_desc.group(1) será "Producto A con color especial"
                match_desc = re.search(r'\]\s*(.*)', description_picking)
                
                # Si se encuentran ambas partes, se fusionan. Si no, se mantiene el nombre original para evitar errores.
                if match_ref and match_desc:
                    supplier_ref = match_ref.group(1)
                    product_description = match_desc.group(1)
                    res['name'] = f"[{supplier_ref}] {product_description}"
                
        return res
