# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com
import re
from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # setting line.name of purchase order line, from procurement values.
    @api.model
    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement(product_id, product_qty, product_uom, location_dest_id, name, origin, company_id, values, po)
        description_picking = values.get('description_picking', False)
        if name:
            res['name'] = name

            codigo_proveedor = False
            # Se busca la descripción del producto en 'description_picking', que está después del salto de línea.
            match_desc = re.search(r'\n\s*(.*)', description_picking)
            # Nombre_producto
            match_nombre_producto = re.search(r'\[.*?\]\s*([^\n]*)', name)
            # Código del proveedor
            if product_id.seller_ids:
                codigo_proveedor = product_id.seller_ids[0].product_code
            # Si se encuentran todas las partes partes, se fusionan. Si no, se mantiene el nombre original para evitar errores.
            if codigo_proveedor and match_desc and match_nombre_producto:
                product_description = match_desc.group(1)
                nombre_producto = match_nombre_producto.group(1)
                res['name'] = f"[{codigo_proveedor}] {nombre_producto}\n{product_description}"
            elif codigo_proveedor and match_nombre_producto:
                nombre_producto = match_nombre_producto.group(1)
                res['name'] = f"[{codigo_proveedor}] {nombre_producto}"
            else:
                res['name'] = name
                    
        return res
