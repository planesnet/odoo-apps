# Gestión Personalizada de Seguidores en Facturas

Este módulo modifica el comportamiento estándar de Odoo para la gestión de seguidores (`followers`) en las facturas.

## Objetivo

El propósito principal es evitar que Odoo agregue seguidores automáticamente a las facturas, con la excepción del cliente. De esta manera, se logra un chatter más limpio y se asegura que las notificaciones solo lleguen a quienes corresponden, evitando la suscripción automática de usuarios internos como el creador del documento.

## Características

*   **Control de Seguidores en Facturas**: Al crear o validar una factura, el módulo interviene para gestionar la lista de seguidores.
*   **Suscripción Exclusiva del Cliente**: Se asegura de que el único seguidor suscrito a una factura sea el contacto del cliente (`partner_id`).
*   **Operación Transparente**: El módulo no requiere configuración. Su lógica se aplica automáticamente en segundo plano.

## Instalación

1.  Añada el módulo a su ruta de `addons`.
2.  Actualice la lista de aplicaciones desde el modo desarrollador.
3.  Busque e instale el módulo `custom_invoice_followers`.

## Uso

El módulo funciona de forma automática tras su instalación.

1.  Cree una nueva factura de cliente o proveedor.
2.  Al guardarla o confirmarla, observe el área de seguidores (chatter).
3.  Verá que el único seguidor es el cliente de la factura, y no se han añadido usuarios internos automáticamente.
