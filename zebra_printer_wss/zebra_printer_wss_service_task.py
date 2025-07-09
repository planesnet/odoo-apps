from simple_websocket_server import WebSocketServer, WebSocket
import time
from datetime import datetime
import os

import signal 
import sys
import json
import socket
import threading
import traceback
import logging

logging.basicConfig(
    filename='./log.log',
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class ZebraPrinterWSS(WebSocket):
    def __init__(self, server, sock, address):
        super().__init__(server, sock, address)
        self.clients = {}

        print("Server:" + str(server) + ". Sock:" + str(sock) + ". Address:" + str(address))
 
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
            port = dict_data['printer_port']
            zpl = dict_data['zpl']
         
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

global_sync_websocket_server = None
global_server_thread = None

def _run_sync_server_in_thread(host, port, handler_class):
    """Función que ejecuta el servidor síncrono en un hilo separado."""
    global global_sync_websocket_server
    try:
        # Aquí se crea y se lanza el servidor síncrono.
        # Esto BLOQUEARÁ ESTE HILO SECUNDARIO indefinidamente.
        logger.info(f"[ServerThread] Iniciando WebSocketServer síncrono en {host}:{port}...")
        global_sync_websocket_server = WebSocketServer(host, port, handler_class) # Asumo WebSocketServer existe
        global_sync_websocket_server.serve_forever() # Bloquea este hilo
        logger.info("[ServerThread] WebSocketServer síncrono ha terminado serve_forever.")
    except Exception as e:
        logger.error(f"[ServerThread] Error fatal en hilo de servidor síncrono: {e}", exc_info=True)
    finally:
        logger.info("[ServerThread] Hilo de servidor síncrono finalizado.")

def start_websocket_server_loop(host="0.0.0.0", port=8001):
    """
    Función que inicia el servidor WebSocket síncrono en un HILO SEPARADO.
    Esta función NO debe bloquear el hilo principal del servicio.
    """
    global global_server_thread
    if global_server_thread and global_server_thread.is_alive():
        logger.info("Servidor WebSocket síncrono ya está en ejecución.")
        return

    logger.info(f"Intentando iniciar servidor WebSocket síncrono en hilo: {host}:{port}")
    
    global_server_thread = threading.Thread(
        target=_run_sync_server_in_thread,
        args=(host, port, ZebraPrinterWSS), # Pasa la clase manejadora
        name="SyncWebSocketServerThread"
    )
    global_server_thread.daemon = True # Permite que el programa principal termine si este hilo no se cierra
    global_server_thread.start()
    logger.info(f"Hilo de servidor WebSocket síncrono {global_server_thread.name} iniciado.")

def trabajo_principal():
    logger.info("trabajo_principal(): Llamando a start_websocket_server_loop().")
    start_websocket_server_loop()
    logger.info("trabajo_principal(): start_websocket_server_loop() ha retornado.")

if __name__ == '__main__':
    # Esto te permite probar el script directamente sin instalar el servicio
    logger.info("Script de lógica iniciado directamente para pruebas.")
    trabajo_principal()
    logger.info("Fin del programa")