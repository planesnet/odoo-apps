# Reglas del Agente (Agent Rules)

- **Framework**: Odoo 18.0
- **Prioridades**:
  - Escribir código limpio (Clean Code)
  - Seguir estrictamente las guías oficiales de desarrollo de Odoo (Odoo Guidelines)

## Reglas de Desarrollo para full_delivery_report
- Todo el código Python debe cumplir estrictamente con PEP 8.
- El módulo es para Odoo 18.0, usa la sintaxis y herencias nativas de esta versión.
- No se permiten consultas SQL directas; usa siempre el ORM de Odoo.
- Todos los archivos XML deben estar bien indentados (4 espacios) y usar identificadores claros.
- El código debe estar preparado para pasar auditorías de calidad (linter de Odoo).
