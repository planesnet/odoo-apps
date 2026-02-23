# Spain - Account Reversal Origin Link

Este módulo extiende la funcionalidad de la localización española en Odoo 18 para permitir la trazabilidad legal entre facturas rectificativas y facturas de origen cuando estas últimas no se han generado mediante el flujo nativo de Odoo.

## Características

* **Vinculación Manual**: Añade un botón "Vincular Origen" en facturas rectificativas (borrador) de clientes y proveedores.
* **Asistente Inteligente**: Filtra automáticamente las facturas del mismo partner y compañía que estén asentadas.
* **Copia de Líneas**: Opción para copiar automáticamente todas las líneas de la factura original a la rectificativa si esta se encuentra vacía.
* **Cumplimiento AEAT/SII**: Al establecer el vínculo, se activa el flag `l11n_es_is_reversal`, asegurando que el envío al SII o TicketBAI contenga la referencia al documento rectificado.
* **Trazabilidad**: Registra un mensaje en el chatter vinculando ambos documentos mediante enlaces internos.

## Instalación

1. Suba el módulo a su repositorio de **Odoo.sh** o añádalo a su ruta de `addons`.
2. Actualice la lista de aplicaciones en modo desarrollador.
3. Instale el módulo `l10n_es_account_reversal_origin`.

## Uso

1. Cree una **Factura Rectificativa** (Factura de Abono) de forma manual.
2. Antes de confirmar, haga clic en el botón **"Vincular Origen"** situado en la parte superior.
3. Seleccione la factura original en el asistente.
4. Si desea que el sistema rellene los productos por usted, mantenga marcada la opción **"¿Copiar líneas del origen?"**.
5. Haga clic en **"Vincular y Procesar"**.

---
**Nota técnica:** Este módulo depende de `l10n_es` para asegurar la compatibilidad con los campos requeridos por la normativa española.