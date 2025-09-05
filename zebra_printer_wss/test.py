
import socket
import sys

def print_zebra_test_page(printer_ip, printer_port=9100):
    """
    Envía un comando ZPL a una impresora Zebra para imprimir un texto de prueba.

    Args:
        printer_ip (str): La dirección IP de la impresora Zebra.
        printer_port (int): El puerto de red de la impresora (por defecto 9100).
    """
    # ZPL (Zebra Programming Language) para imprimir un texto de prueba
    # ^XA: Inicia el formato de etiqueta
    # ^FO50,50: Establece el origen del campo (x,y) en 50 puntos desde la esquina superior izquierda
    # ^A0N,60,60: Establece la fuente (A0), orientación normal (N), altura 60, ancho 60
    # ^FD: Inicia el campo de datos
    # ^FS: Finaliza el campo de datos
    # ^XZ: Finaliza el formato de etiqueta
    zpl_command = (
        "^XA"
        "^FO50,50^A0N,60,60^FDPrueba de Impresora Zebra^FS"
        "^FO50,120^A0N,40,40^FDIP: {ip_address}^FS"
        "^FO50,170^A0N,40,40^FDConexion Exitosa!^FS"
        "^XZ"
    ).format(ip_address=printer_ip)

    print(f"Intentando conectar a la impresora en {printer_ip}:{printer_port}...")

    try:
        # Crea un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta al puerto de la impresora
            s.connect((printer_ip, printer_port))
            print("Conexión establecida. Enviando comandos ZPL...")

            # Envía el comando ZPL codificado en bytes
            s.sendall(zpl_command.encode('utf-8'))
            print("Comandos ZPL enviados exitosamente.")
            print("Por favor, revisa la impresora para el texto de prueba.")

    except socket.error as e:
        print(f"Error de conexión o envío: {e}")
        print("Asegúrate de que la impresora esté encendida, conectada a la red y que la IP sea correcta.")
        print("También verifica que no haya un firewall bloqueando el puerto 9100.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # La dirección IP de tu impresora Zebra
    PRINTER_IP_ADDRESS = "10.0.10.230"
    
    # Llama a la función para imprimir la página de prueba
    print_zebra_test_page(PRINTER_IP_ADDRESS)

