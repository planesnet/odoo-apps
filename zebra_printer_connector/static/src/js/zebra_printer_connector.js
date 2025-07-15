/** @odoo-module */

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

class AccionImprimirEtiqueta extends Component {

    static template = "zebra_printer_connector.AccionImprimirEtiquetaTemplate";

    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
        this.notification = useService("notification");

        this.context = this.props.action.context || {};
        this.resId = this.context['active_id']
        this.modelName = this.context['model_name']
        this.reportName = this.context['report_name']
        this.printerIp = this.context['printer_ip']
        this.printerPort = this.context['printer_port']
        this.proxyServerIp = this.context['proxy_server_ip']
        this.proxyServerPort = this.context['proxy_server_port']
        this.printerResolution = this.context['printer_resolution']
        this.bultos = this.context['bultos']

        this._executePrintAction();

        //this.connectToWebSocketServer();
    }

    // --- Nueva función asíncrona para encapsular la lógica principal ---
    async _executePrintAction() {
        // Validación básica de campos necesarios antes de continuar
        if (!this.printerIp || !this.printerPort || !this.proxyServerIp || !this.proxyServerPort) {
            this.notification.add("Faltan parámetros de configuración de impresora o proxy.", { type: "danger" });
            this.closeClientAction();
            return;
        }

        // 1. Obtener el ZPL de la etiqueta desde Python
        try {
            this.notification.add("Generando ZPL de la etiqueta...", { type: "info" });
            this.zpl = await this.orm.call("ir.actions.report", "get_zpl", [
                this.resId,
                this.modelName,
                this.reportName,
                this.bultos,
                this.printerResolution
            ]);

            if (!this.zpl) {
                this.notification.add("El ZPL no pudo ser generado. Verifique la configuración del reporte.", { type: "danger" });
                this.closeClientAction();
                return;
            }
            console.log("ZPL obtenido:", this.zpl);

        } catch (error) {
            this.notification.add(`Error al obtener ZPL: ${error.message || error.data.message || error}`, { type: "danger" });
            console.error("Error al obtener ZPL:", error);
            this.closeClientAction();
            return;
        }

        // 2. Conectar e Imprimir
        try {
            this.notification.add("Conectando al servidor de impresión WSS...", { type: "info" });
            // Llama a la nueva función asíncrona para conectar y enviar
            await this.connectAndSendToWebSocketServer();
        } catch (error) {
            // Este catch manejará los errores de conexión o envío
            this.notification.add(`Error crítico de conexión o envío al servidor WSS: ${error.message || error.data.message || error}`, { type: "danger" });
            console.error("Error crítico en conexión WSS:", error);
            this.closeClientAction();
        }
    }

    async connectAndSendToWebSocketServer() { // <-- Ahora es async para usar await en la conexión
        const url = "wss://" + this.proxyServerIp + ":" + this.proxyServerPort.toString();
        console.log(url);
        this.ws = new WebSocket(url);

        return new Promise((resolve, reject) => {
            this.ws.onopen = (event) => {
                this.notification.add("Conexión WSS establecida. Enviando datos...", { type: "success" });
                console.log("WebSocket onopen: Conexión establecida.");
                this.sendToWebSocketServer(); // Llamar a send una vez que la conexión esté abierta
                resolve(); // Resuelve la promesa al abrir
            };

            this.ws.onmessage = (event) => {
                var result;
                try {
                    result = JSON.parse(event.data);
                } catch (e) {
                    console.error("Error al parsear JSON del WebSocket:", e, "Datos:", event.data);
                    this.notification.add("Error al procesar respuesta del servidor de impresión.", { type: "danger" });
                    return;
                }
                
                if (result.code === 'ERROR') { // Usar === para comparación estricta
                    this.notification.add(`Error de impresión: ${result.message}`, { type: "danger" });
                    console.error("Error del servidor WebSocket:", result.message);
                } else if (result.code === 'OK') {
                    this.notification.add("Etiqueta enviada correctamente.", { type: "success" });
                    console.log("WebSocket onmessage: Operación OK.");
                } else {
                    this.notification.add(`Respuesta inesperada del servidor: ${event.data}`, { type: "warning" });
                    console.warn("Respuesta WebSocket inesperada:", event.data);
                }
                this.closeClientAction(); // Cerrar la acción después de recibir respuesta
                resolve(); // Resolver la promesa también al recibir mensaje (si esperas solo uno)
            };

            this.ws.onerror = (event) => {
                const errorMessage = "No hay conexión con el servidor WSS de impresión. Asegúrese de que esté encendido y que el certificado autofirmado haya sido aceptado en su navegador.";
                this.notification.add(errorMessage, { type: "danger", sticky: true }); // sticky para que permanezca
                console.error("WebSocket onerror:", event);
                reject(new Error("Conexión WSS fallida o error.")); // Rechaza la promesa en caso de error
            };

            this.ws.onclose = (event) => {
                // Solo loguea si no es un cierre normal después de que la lógica terminó
                if (!event.wasClean) {
                    this.notification.add("Conexión WSS cerrada inesperadamente.", { type: "warning" });
                    console.warn("WebSocket onclose: Conexión cerrada inesperadamente.", event.code, event.reason);
                } else {
                    console.log("WebSocket onclose: Conexión cerrada limpiamente.");
                }
                // Si la acción no se ha cerrado ya, podrías cerrarla aquí.
                // self.closeClientAction();
            };
        });
    }

    sendToWebSocketServer() { // Ya no necesita 'self' como parámetro si usa 'this' directamente
        console.log("Estado del WebSocket antes de enviar:", this.ws.readyState);
        if (this.ws.readyState === WebSocket.OPEN) {
            console.log("ZPL a enviar:", this.zpl);

            var send_data = {
                'zpl': this.zpl,
                'printer_ip': this.printerIp,
                'printer_port': this.printerPort
            }
            this.ws.send(JSON.stringify(send_data)); // Usa 'this'
            console.log("Datos enviados al servidor WebSocket.");
            // No cierres la acción aquí; espera la respuesta en onmessage
        } else {
            console.error("WebSocket no está abierto. Estado:", this.ws.readyState);
            this.notification.add("Error interno: WebSocket no está listo para enviar datos.", { type: "danger" });
            // Rechazar la promesa si no está abierto (si se usara en un try/catch)
        }
    }

    closeClientAction() {
        this.action.restore();
        //this.action.doAction("stock.product_template_action_product");
    }

    /*
    async connectToWebSocketServer() {
        var self = this;

        //Primero obtenemos el ZPL de la etiqueta, renderizando la plantilla desde un método Python
        this.zpl = await this.orm.call("ir.actions.report", "get_zpl", [this.resId, this.modelName, this.reportName, this.bultos, this.printerResolution]);

        if (this.zpl != null && this.printerIp != null && this.printerPort != null && this.proxyServerIp != null && this.proxyServerPort) {
            var url = "wss://" + this.proxyServerIp + ":" + this.proxyServerPort.toString();
            this.ws = new WebSocket(url);

            this.ws.onmessage = (event) => {
                var result = JSON.parse(event.data);
                if (result['code'] == 'ERROR') {
                    alert("Error: " + result['message']);    
                }
                else {
                    console.log("WebSocket onmessage");
                }
            };
            this.ws.onerror = (event) => {
                alert("No hay conexión con el servidor WSS de impresión. Seguramente este apagado o se encuentre en un estado incorrecto. Por favor, enciéndalo y vuelva a intentarlo.");
            };

            //Hay que dar algo de tiempo para que conecte el WebSocket desde esta versión en JS.
            setTimeout(function() {
                self.sendToWebSocketServer(self);
            }, 1000);
        }
    }

    sendToWebSocketServer(self) {
        console.log(self.ws.readyState);
        if (self.ws.readyState === WebSocket.OPEN) {
            console.log(this.zpl);

            var send_data = {
                'zpl': this.zpl,
                'printer_ip': this.printerIp,
                'printer_port': this.printerPort
            }
            self.ws.send(JSON.stringify(send_data));

            self.closeClientAction();
        }
    }*/
}
registry.category("actions").add("zebra_printer_connector.AccImpEti", AccionImprimirEtiqueta);