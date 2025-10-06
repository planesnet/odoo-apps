# -*- coding: utf-8 -*-
# Copyright 2025 planesnet.com

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
                #name contiene la ref del proveedor y description_picking contiene la descripción modificada para la venta (añadiendo por ej un color especial)
                #y queremos que esa información llegue al pedido de compra, por lo que lo fusionamos

                # Tomamos todo el texto después del corchete de cierre ']'
                # El método find() localiza la posición del carácter y le sumamos 2 para omitir el corchete y el espacio
                parte_description_picking = description_picking[description_picking.find(']') + 2:]

                # Del name, extraemos solo el texto que está entre los corchetes
                # Sumamos 1 a la posición del primer corchete para no incluirlo
                # y usamos la posición del segundo como final del rebanado
                parte_name = name[name.find('[') + 1:name.find(']')]

                # Fusionamos ambas partes
                res['name'] = '[' + parte_name + '] ' + parte_description_picking
                
        return res
