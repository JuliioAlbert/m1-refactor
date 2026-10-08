# Aprendizajes y conclusiones

**Nombre:** Julio Alberto Gonzalez de Jesus · **Fecha:** 2026-10-07

## Utilidad de Claude Code

Claude Code fue muy útil para detectar y corregir los code smells de `src/`. En 7 refactorizaciones (código muerto, type hints, extracción de funciones, manejo de errores, condicionales, renombres e imports) los tests siguieron en `✅ 20 passed` y ruff bajó de 13 errores a 0. Lo más valioso fue que cada cambio quedó acotado en un plan de `specs/`, una rama, un commit atómico y una fila de la bitácora, así que todo es trazable y reversible.

## Qué propuso la IA que no había notado

- `registrar_venta` y `cotizar` duplicaban la lógica de descuento; se compartió con `_descuento_volumen`.
- `almacen` tenía fugas de archivos (sin `with open`), `except Exception` que ocultaba bugs y estado a medias si el JSON venía mal formado.
- Números mágicos (IVA 16%, tramos de descuento) que pasaron a constantes (`TASA_IVA`, umbrales).
- Nombres crípticos como `hacer_cosa`, `aux`, `temp`, `d`, `s` y `t`.

## Dónde tuve que corregir o rechazar

<!-- COMPLETA con tu experiencia real. Ejemplos de qué anotar:
- Alcance de "mejorar manejo de errores" (acoté a estructural + caminos de falla).
- Algún cambio que alteraba el comportamiento observable o el formato del ticket.
- Renombres que chocaban con `agregarProducto`/`buscarProducto` (los tests los usan).
- Estado global de `gestor` que debía seguir reiniciable por `reiniciar_sistema()`. -->

## Qué aprendí sobre refactorizar con IA

1. Los tests de caja negra son la red de seguridad. Sin ellos, la IA podría cambiar el comportamiento sin que me diera cuenta.
2. Conviene pedir cambios pequeños y de un solo tipo por plan. Los commits atómicos hacen fácil revisar y revertir.
3. Hay que correr `pytest` y `ruff check src` después de cada paso, no solo al final.
4. Planear antes de aplicar (scope, criterios de aceptación, decisiones) evita que la IA se pase del alcance.
5. La IA propone y yo decido. Revisar el diff sigue siendo mi responsabilidad, sobre todo en reglas de negocio (descuento por volumen, VIP, IVA, formato del ticket).
