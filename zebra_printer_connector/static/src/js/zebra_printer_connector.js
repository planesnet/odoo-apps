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

        this.connectToWebSocketServer();
    }

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
    }

    closeClientAction() {
        this.action.restore();
        //this.action.doAction("stock.product_template_action_product");
    }
}
registry.category("actions").add("zebra_printer_connector.AccImpEti", AccionImprimirEtiqueta);