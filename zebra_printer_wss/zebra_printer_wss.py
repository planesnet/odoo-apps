from simple_websocket_server import WebSocketServer, WebSocket
from optparse import OptionParser

import time
import random
import signal 
import sys
import socket
import json
import logging
import threading
import traceback

import logging
logger = logging.getLogger(__name__)

class ZebraPrinterWSS(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.clients = {}
 
    def get_remote_print(self, data):
        print("get_remote_print method executed!!")
        try:
            # Actualizar la última impresora seleccionada.
            # user = self.env['res.users'].search([('id','=',self.env.uid)])
            # if user and (( user.printer_id and user.printer_id != self) or (not user.printer_id)):
            #     user.write({'printer_id':self.id})

            #One easy way to find the IP address is with this nmap command
            # nmap  192.168.0.* -p T:9100 --open

            dict_data = json.loads(data)
            ip = dict_data['printer_ip']
            zpl = dict_data['zpl']
         
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = 9100
            s.connect((ip, port))
            logger.info("Connect at %s:%s" % (ip,str(port)))

            logger.info("Send data to printer. \n%s" % (zpl))
            zpl = str(zpl.encode("utf-8"), "utf-8").encode("ascii","ignore")
            s.send(bytes(zpl))

            s.close()
            logger.info("End of label print")

        except Exception as e:
            ex_type, ex, tb = sys.exc_info()
            logger.error(traceback.extract_tb(tb))
            try:
                s.close()
            except Exception:
                pass
            raise e

        except Exception as ex:
            return "ERROR"
        finally:
            pass

        return "OK"

    def handle(self):
        state = False
        try:
            logger.info("Petición solicitada!")
            state = self.get_remote_print(self.data)

            for k in self.clients.keys():
                client = self.clients.get(k)
                logger.info("{} Estado petición:{}".format(self.address[1], state))
                client.send_message(json.dumps({'code': state, 'message': ''}))

        except Exception as ex:
            logger.error(ex, exc_info=True)
            self.clients.get(list(self.clients.keys())[0]).send_message(json.dumps({'code': 'ERROR', 'message': str(ex)}))

    def connected(self):
        try: 
            self.clients.update({self.address[1]: self})

            if(len(self.clients.keys())>0):
                logger.info("Clientes conectados:")

            for k in self.clients.keys():
                client = self.clients.get(k)
                logger.info("{} Cliente conectado.".format(client.address[1]))

        except Exception as ex:
            logger.error(ex, exc_info=True)

    def handle_close(self):
        try:
            logger.info("{} Solicitud de desconexión".format(self.address[1]))
            con = self.clients.get(self.address[1], False)
            if con:
                logger.info("Cliente desconectado ({})".format(self.address[1]))
                con.close()

        except Exception as ex:
            logger.error(ex, exc_info=True)

if __name__=="__main__":


    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    

    parser = OptionParser(usage='usage: %prog [options]', version='%prog 1.0')
    parser.add_option('--host', default='', type='string', action='store', dest='host', help='IP Address)')
    parser.add_option('--port', default=5000, type='int', action='store', dest='port', help='port (5000)')
    parser.add_option('--simulate', action='store_true', dest='simulate', default=False, help='Simulation')
    parser.add_option("--debug", action="store_true", dest="verbose", default=False, help="detail log for proxy.")


    (options, args) = parser.parse_args()

    server = WebSocketServer('127.0.0.1', 5001, ZebraPrinterWSS)

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    if options.verbose:
        logger.setLevel(logging.DEBUG)

    server.serve_forever()

    logger.info("Fin del programa")