# Bitácora de refactorización

**Nombre:** Julio Gonzalez
**Matrícula:**
**Fecha:** 2026-10-07

Registra aquí **cada refactorización** que realices con Claude Code. Copia el
prompt tal cual lo escribiste (o un resumen fiel si fue una conversación larga),
describe el cambio que se aplicó al código y justifica por qué mejora la calidad.
Después de cada cambio ejecuta `pytest` y anota el resultado.

| #  | Prompt usado | Cambio realizado | Justificación | Tests OK |
|----|--------------|------------------|---------------|----------|
| 1  |  Eliminar código muerto y comentarios obsoletos de `src/` sin cambiar comportamiento | Se borran `MODO_DEBUG`, `calcular_descuento_viejo`, `exportar_txt` comentado, `import os` sin uso, `reporteViejoCSV`, cabeceras `# -*- coding -*-` y frase obsoleta del docstring. Plan: [specs/eliminar-codigo-muerto.md](specs/eliminar-codigo-muerto.md) (commit 3392724) | Menos ruido y código no referenciado; elimina errores ruff F401, ERA001, UP009, N802 (1) y SIM115 | ✅ 20 passed |
| 2  | Agregar type hints a funciones | Type hints en todas las funciones de `src/`, `TypedDict` `Producto`/`Venta` y globals anotados. Plan: [specs/agregar-type-hints.md](specs/agregar-type-hints.md) | Contratos implícitos (dicts sin forma, retornos `X \| None`) quedan explícitos; habilita chequeo estático y autocompletado sin cambiar comportamiento | ✅ 20 passed; ruff 13 errores (sin cambio) |
| 3  | Extraer funciones de código duplicado o bloques muy largos | `registrar_venta` partida en `_validar_venta`/`_descuento_volumen`/`_es_vip`/`_armar_ticket` (descuento compartido con `cotizar`); `menu` despachado por funciones por opción; `reportes` reusa `total_vendido` y `_stock_bajo`. Plan: [specs/extraer-funciones.md](specs/extraer-funciones.md) | Elimina Long Method y código duplicado; quita ruff C901 (×2), SIM102 (×3) y SIM108 | ✅ 20 passed; ruff 7 errores (antes 13) |
| 4  | Mejorar manejo de errores (alcance: estructural + caminos de falla) | `with open` + excepciones acotadas y validación de forma antes de mutar estado en `almacen`; `main` revisa retornos de cargar/guardar y valida enteros finitos (`pedir_entero`); motivos de error como constantes `ERROR_*` en `gestor`. Plan: [specs/mejorar-manejo-de-errores.md](specs/mejorar-manejo-de-errores.md) | Elimina fuga de archivos, `except Exception` que oculta bugs, estado a medias, mensajes engañosos y tracebacks por entrada; quita ruff SIM115 (×2) y UP015 | ✅ 20 passed; ruff 4 errores (antes 7) |
| 5  | Simplificar condicionales complejos | Condiciones con nombre (`_cantidad_invalida`, `_descuento_vip`, `startswith`), tramos de descuento y umbrales como constantes, guard clauses en `main`, `hayArchivo` retorna directo. Plan: [specs/simplificar-condicionales.md](specs/simplificar-condicionales.md) | Elimina condicionales duplicados/complejos y números mágicos; quita ruff SIM103 | ✅ 20 passed; ruff 3 errores (antes 4) |
| 6  | Renombrar variables o funciones para mayor claridad | Nombres descriptivos en `src/` (`hacer_cosa`→`formato_dinero`, `hayArchivo`→`existe_archivo`, `contadorVentas`→`contador_ventas`, `aux/temp/d/s/t`→nombres de intención, constante `TASA_IVA`). Plan: [specs/renombrar-variables.md](specs/renombrar-variables.md) | Elimina nombres crípticos y números mágicos; quita ruff N802 y N816 | ✅ 20 passed; ruff 1 error (antes 3) |
| 7  | Reparar el import | Imports de `main.py` en orden alfabético (`almacen`, `gestor`, `reportes`). Plan: [specs/ordenar-imports.md](specs/ordenar-imports.md) | Elimina imports sin ordenar; quita ruff I001 | ✅ 20 passed; ruff 0 errores (antes 1) |

> Agrega más filas si realizas más de 5 refactorizaciones.

## Reflexión final (10-15 líneas)

Responde: ¿Qué tan útil fue Claude Code para detectar y corregir los problemas?
¿Qué propuso la IA que tú no habías notado? ¿En qué casos tuviste que corregir
o rechazar sus sugerencias? ¿Qué aprendiste sobre refactorizar con apoyo de IA?

*(Escribe aquí tu reflexión)*
