# Nombre del fichero: wss_service_handler.py
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import os
import asyncio
import threading

# Importa la lógica del servidor desde el otro fichero
# Asegúrate de que wss_server_for_service.py está en la misma carpeta
# o en una ruta accesible por Python.
from proxy_server import main as wss_main

# Cambia el directorio de trabajo al del script.
# Esto es crucial para que el servicio encuentre los ficheros (cert.pem, etc.).


path = os.path.dirname(os.path.abspath(__file__))
print(f"PATH {path}")
os.chdir(path)

class WSServerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WSSPythonServer"
    _svc_display_name_ = "WSS Python Server"
    _svc_description_ = "Servidor WebSocket Secure implementado en Python que se ejecuta como servicio de Windows."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False
        self.async_loop = None
        self.server_thread = None
        self.stop_event = None

    def SvcStop(self):
        """Llamado cuando el servicio recibe la señal de detenerse."""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Señala al evento principal que debe detenerse
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True
        
        # Señala al bucle de asyncio que se detenga
        if self.async_loop and self.stop_event:
            self.async_loop.call_soon_threadsafe(self.stop_event.set)

    def SvcDoRun(self):
        """El método principal del servicio."""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        
        self.main()

        # Espera a que el hilo del servidor termine antes de salir
        if self.server_thread:
            self.server_thread.join()

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))

    def main(self):
        """Lógica principal para iniciar el servidor en un hilo separado."""
        self.async_loop = asyncio.new_event_loop()
        self.stop_event = asyncio.Event()
        
        # El servidor asyncio se ejecuta en un hilo separado para no bloquear el servicio
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

        # El servicio espera aquí hasta que SvcStop señale el evento
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def run_server(self):
        """Configura y ejecuta el bucle de eventos de asyncio."""
        asyncio.set_event_loop(self.async_loop)
        try:
            self.async_loop.run_until_complete(wss_main(self.stop_event))
        finally:
            self.async_loop.close()


if __name__ == '__main__':
    # Permite gestionar el servicio desde la línea de comandos
    win32serviceutil.HandleCommandLine(WSServerService)
