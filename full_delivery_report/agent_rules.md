# Reglas del Agente (Agent Rules)

- **Framework**: Odoo (la versión correspondiente a la rama de Git activa en cada momento: 17.0, 18.0 o 19.0)
- **Prioridades**:
  - Escribir código limpio (Clean Code)
  - Seguir estrictamente las guías oficiales de desarrollo de Odoo (Odoo Guidelines)

## Reglas de Desarrollo para full_delivery_report
- Todo el código Python debe cumplir estrictamente con PEP 8.
- El módulo debe adaptarse dinámicamente a la versión de Odoo correspondiente a la rama de Git activa (17.0, 18.0 o 19.0), usando la sintaxis y herencias nativas de dicha versión.
- No se permiten consultas SQL directas; usa siempre el ORM de Odoo.
- Todos los archivos XML deben estar bien indentados (4 espacios) y usar identificadores claros.
- El código debe estar preparado para pasar auditorías de calidad (linter de Odoo).
