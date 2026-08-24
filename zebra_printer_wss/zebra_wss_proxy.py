# Nombre del fichero: wss_server_for_service.py
import asyncio
import ssl
import websockets
import json
import logging
import socket

# --- Configuración del Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    # Opcional: Escribe logs a un fichero si lo necesitas para depuración
    # handlers=[
    #     logging.FileHandler("c:/WSS_Service/server_log.txt"),
    #     logging.StreamHandler()
    # ]
)
logger = logging.getLogger(__name__)

async def handler(websocket):
    """Gestiona las conexiones WebSocket entrantes."""
    logger.info(f"Cliente conectado desde {websocket.remote_address}")
    try:
        async for message in websocket:
            response = {}
            try:
                data = json.loads(message)
                if isinstance(data, dict):
                    logger.info("Diccionario recibido correctamente:")
                    printer_ip = data['printer_ip']
                    printer_port = data['printer_port']
                    zpl_data = data['zpl']
                    # logger.info(json.dumps(data, indent=4, ensure_ascii=False))

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((printer_ip, printer_port))
                
                    # Prepara ZPL (asumiendo que zpl_data es un string Unicode)
                    zpl_bytes = zpl_data.encode("utf-8", errors="ignore") 
                    s.sendall(zpl_bytes) # Asegura que todos los bytes se envíen
                    s.close()
                    response = {"code": "OK", "message": "Diccionario recibido."}
                else:
                    logger.warning(f"Dato recibido no es un diccionario: {data}")
                    response = {"code": "ERROR", "message": "El dato recibido no es un diccionario."}
            except json.JSONDecodeError:
                logger.error(f"Error: Mensaje recibido no es un JSON válido: {message}")
                response = {"code": "ERROR", "message": "El mensaje no es un JSON válido."}
            except Exception as e:
                logger.error(f"Error procesando el mensaje: {e}")
                response = {"code": "ERROR", "message": f"Error inesperado en el servidor: {e}"}
            
            await websocket.send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Cliente desconectado: {e.code} {e.reason}")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado en la conexión: {e}")
        if websocket.open:
            error_response = {"code": "ERROR", "message": "Error interno del servidor."}
            await websocket.send(json.dumps(error_response))

async def main(stop_event, certfile="cert.pem", keyfile="key.pem", host="0.0.0.0"):
    """
    Configura y arranca el servidor WSS.
    Acepta un evento 'stop' para poder detenerse de forma controlada.
    """
    port = 8765
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        # Usamos las rutas pasadas como argumentos (por defecto buscan en el CWD)
        ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    except FileNotFoundError:
        logger.critical(f"Error: No se encontraron los ficheros '{certfile}' y '{keyfile}'.")
        return

    logger.info(f"Iniciando servidor WSS en {host}:{port}")
    
    # Inicia el servidor y lo mantiene corriendo hasta que el evento 'stop_event' se active.
    async with websockets.serve(handler, host, port, ssl=ssl_context):
        await stop_event.wait()
    
    logger.info("Servidor WSS detenido.")

if __name__ == '__main__':
    # Esta sección es solo para probar el servidor directamente, no se usa cuando se ejecuta como servicio.
    print("Ejecutando servidor en modo de prueba. Presiona Ctrl+C para detener.")
    stop = asyncio.Event()
    try:
        asyncio.run(main(stop))
    except KeyboardInterrupt:
        print("Deteniendo servidor...")
        stop.set()
