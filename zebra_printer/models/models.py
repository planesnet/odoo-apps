# -*- coding: utf-8 -*-
from odoo import models, fields, api
import socket
import sys, traceback
import logging
_logger = logging.getLogger(__name__)

RESOLUCIONES = [
    ('203', '203 ppp'),
    ('300', '300 ppp')
]

class ZebraPrinter(models.Model):
    _name = "zebra.printer"
    _description = "Zebra printers"

    name = fields.Char('Name' , index=True)
    model = fields.Selection([
        ('default', 'Default'),
        ('gx430t', 'GX430t'),
    ], required=True, default='default')

    ip = fields.Char('IP number')
    port = fields.Integer('Port', default=9100)
    buffer_size = fields.Integer('Buffer size', default=1024)
    resolution = fields.Selection(RESOLUCIONES, string="Resolución (ppp)", default='300')
    active = fields.Boolean(default=True)

    def zprint(self, datas):
        self.ensure_one()

        # Actualizar la última impresora seleccionada.
        # user = self.env['res.users'].search([('id','=',self.env.uid)])
        # if user and (( user.printer_id and user.printer_id != self) or (not user.printer_id)):
        #     user.write({'printer_id':self.id})

        #One easy way to find the IP address is with this nmap command
        # nmap  192.168.0.* -p T:9100 --open
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip, self.port))
            _logger.info("Connect with %s at %s:%s" % (self.name, self.ip,str(self.port)))

            for data in datas:

                zpl = data.getZPL()
                _logger.debug("Send data to printer %s. \n%s" % (self.name, zpl))
                zpl = str(zpl.encode("utf-8"), "utf-8").encode("ascii","ignore")
                s.send(bytes(zpl))

            s.close()
            _logger.debug("End of label print")


        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            _logger.error(traceback.extract_tb(tb))
            try:
                s.close()
            except Exception:
                pass
            raise e


# Permite guardar la última impresora utilizada por un suario.
class ResUsers(models.Model):
    _inherit = 'res.users'

    printer_id = fields.Many2one('zebra.printer', string='Last printer', help="Ultima impresora seleccioanda")
