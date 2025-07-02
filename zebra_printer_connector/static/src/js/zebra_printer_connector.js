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

        this.connectToWebSocketServer();
    }

    async connectToWebSocketServer() {
        var self = this;

        //Primero obtenemos el ZPL de la etiqueta, renderizando la plantilla desde un método Python
        this.zpl = await this.orm.call("ir.actions.report", "get_zpl", [this.resId, this.modelName, this.reportName]);

        if (this.zpl != null && this.printerIp != null && this.printerIp != '0.0.0.0') {
            var url = "ws://127.0.0.1:5001";
            this.ws = new WebSocket(url);

            this.ws.onmessage = (event) => {
                console.log("WebSocket onmessage")
            };
            this.ws.onerror = (event) => {
                var value = event.data;
                console.log("WebSocket onerror");
                console.log("Value=" + value);
                console.log(event);
            };

            //Hay que dar algo de tiempo para que conecte el WebSocket desde esta versión en JS.
            setTimeout(function() {
                self.sendToWebSocketServer(self);
            }, 1000);
        }
    }

    sendToWebSocketServer(self) {
        if (self.ws.readyState === WebSocket.OPEN) {
            console.log(this.zpl);

            var send_data = {
                'zpl': this.zpl,
                'printer_ip': this.printerIp
            }
            self.ws.send(JSON.stringify(send_data));
        }
        else {
            console.log(0);
        }
        self.closeClientAction();      
    }

    closeClientAction() {
        this.action.restore();
        //this.action.doAction("stock.product_template_action_product");
    }
}
registry.category("actions").add("zebra_printer_connector.AccImpEti", AccionImprimirEtiqueta);