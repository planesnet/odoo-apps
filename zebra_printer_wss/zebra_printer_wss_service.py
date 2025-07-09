# mi_servicio.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import time
import logging

# Importamos la lógica de nuestro otro archivo
from zebra_printer_wss_service_task import trabajo_principal

logging.basicConfig(
    filename='./log.log',
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

class ZebraPrinterWSSService(win32serviceutil.ServiceFramework):
    """
    Clase para definir nuestro servicio de Windows.
    """
    # Nombre interno del servicio.
    _svc_name_ = "ZebraPrinterWSS_Service"
    # Nombre que se mostrará en la lista de servicios de Windows.
    _svc_display_name_ = "ZebraPrinterWSS_Service servicio"
    # Descripción del servicio.
    _svc_description_ = "Servicio para el Servidor de impresión por WSS para la impresión por impresora Zebra"

    def __init__(self, args):
        """
        Constructor del servicio.
        """
        logger.info('ZebraPrinterWSSService::__init__::Inicio')

        win32serviceutil.ServiceFramework.__init__(self, args)
        # Creamos un evento para poder detener el servicio.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        """
        Método que se llama cuando el servicio recibe la señal de detenerse.
        """
        logger.info('El servicio ha recibido una solicitud de parada.')
        # Indicamos al Administrador de Control de Servicios que estamos en proceso de parada.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Activamos el evento que hará que el bucle principal termine.
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        """
        Método principal del servicio. Aquí se ejecuta la lógica.
        """
        logger.info('Entrando SvcDoRun.')
        # Escribimos en el log que el servicio se ha iniciado.
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        logger.info('Servicio iniciado.')

        # Bucle principal que se ejecuta mientras el servicio esté activo.
        try:
            # Llamamos a la función que contiene la lógica de nuestro programa.
            trabajo_principal()
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE) 

        except Exception as e:
            # Si ocurre un error, lo escribimos en el log para poder depurarlo.
            logger.info(f'Error en el servicio: {e}')
            time.sleep(5) # Esperamos un poco antes de reintentar

        logger.info('El servicio se ha detenido.')

if __name__ == '__main__':
    # Esto permite manejar el servicio desde la línea de comandos
    # para instalar, iniciar, detener, etc.

    logger.info("__main__::Inicio")
    win32serviceutil.HandleCommandLine(ZebraPrinterWSSService)
    logger.info("__main__::Despues de HandleCommandLine")
