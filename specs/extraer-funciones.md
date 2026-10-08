# Extraer funciones de código duplicado o bloques muy largos

## Context
`registrar_venta` (gestor.py:105, C901 12) mezcla validación anidada, descuentos, IVA, stock, folio y ticket; `cotizar` duplica el cálculo de descuento por volumen. `menu` (main.py:20, C901 17) es un `if/elif` gigante con `print("Error:", gestor.ultimo_error)` repetido 3 veces. `reportes.resumen_ventas` re-suma totales que ya calcula `total_vendido`, y el umbral `< 5` de stock bajo está duplicado. Objetivo: funciones pequeñas con una responsabilidad, sin duplicación, comportamiento idéntico. Al implementar, este plan se guarda como `specs/extraer-funciones.md`.

## Scope
Solo `src/gestor.py`, `src/main.py`, `src/reportes.py`. Nada en `tests/`, `pyproject.toml`, `almacen.py`. Sin cambiar nombres públicos, mensajes, orden de errores ni formato de ticket/reportes.

**gestor.py** (helpers privados `_`):
- `_validar_venta(codigo, cantidad) -> Producto | None`: guard clauses planas en el mismo orden de errores (codigo vacio → producto no existe → cantidad invalida → stock insuficiente); fija `ultimo_error`.
- `_descuento_volumen(subtotal) -> float`: >=1000 → 10%, >=500 → 5%, si no 0 (int, como hoy). Usado por `registrar_venta` **y** `cotizar`.
- `_es_vip(cliente) -> bool`: `bool(cliente) and cliente.startswith("VIP")` (equivale a `!= "" and not None and len>=3 and [0:3]=="VIP"`).
- `_armar_ticket(venta) -> str`: mismo texto línea por línea; línea "Descuento" si `venta["descuento"] > 0`.
- `registrar_venta` queda: validar → subtotal → descuento volumen (+2% si `_es_vip` y `subtotal-desc > 200`) → IVA → stock/folio → dict venta → ticket → append.
- `cotizar` usa `_descuento_volumen` (sigue SIN extra VIP, como hoy).

**main.py**:
- `_mostrar_error()` → `print("Error:", gestor.ultimo_error)`.
- `_imprimir_opciones()` (las 8 líneas del menú + línea vacía).
- Una función por opción: `_opcion_agregar_producto`, `_opcion_registrar_venta`, `_opcion_cotizar`, `_opcion_mas_vendidos`, `_opcion_stock_bajo`; opciones 4/5 apuntan directo a `reportes.reporte_inventario`/`resumen_ventas`.
- Dict `ACCIONES = {"1": ..., "7": ...}`; `menu` despacha con `ACCIONES.get(op)`, "8" guarda y `break`, otro → "Opcion no valida.".

**reportes.py**:
- `_stock_bajo(p) -> bool` (`p["stock"] < 5`) usado en `productos_stock_bajo` y `reporte_inventario`.
- `resumen_ventas` usa `total_vendido()` en vez de su propio acumulador.

Fuera de alcance: renombrar `hacer_cosa`/`hayArchivo`/`contadorVentas`, constantes para números mágicos, `with open`, burbuja → `sorted`, I001 (otros planes).

## Scores genéricos
- Riesgo: 2/5 (ticket, menú y redondeos sin tests de caja negra completos → verificación manual)
- Impacto en legibilidad/mantenibilidad: 5/5
- Esfuerzo: 3/5
- Errores ruff: 13 → 7 (desaparecen C901×2, SIM102×3, SIM108×1)

## Implementation plan
1. `git checkout -b refactor/extraer-funciones` desde `main`.
2. Antes de tocar código: capturar snapshot de salida (script en scratchpad que registra ventas normal/medio/alto/VIP, imprime tickets con fecha fija vía monkeypatch de `gestor.datetime`, cotizaciones, `reporte_inventario`, `resumen_ventas`, `mas_vendidos`, casos de error y `ultimo_error`) → `antes.txt`. Igual para el menú: `printf` con opciones 1–8 + inválida → `menu_antes.txt` (cwd = scratchpad).
3. Crear `specs/extraer-funciones.md` con este plan.
4. Refactor `gestor.py`; `pytest` + `ruff check src`.
5. Refactor `reportes.py`; `pytest` + `ruff`.
6. Refactor `main.py`; `pytest` + `ruff`.
7. Repetir snapshots → `diff` vacío contra los de antes.
8. Llenar fila #3 de `BITACORA.md`.
9. Commit atómico `refactor: extraer funciones de código duplicado y bloques largos` (src + spec + bitácora) con trailer Co-Authored-By; `git push -u origin refactor/extraer-funciones`.

## Acceptance criteria
- Ninguna función de `src/` con C901; `registrar_venta` y `menu` sin anidamiento > 2.
- Lógica de descuento por volumen en un solo lugar; `"Error:"` impreso en un solo lugar.
- `pytest`: 20 passed, tests intactos.
- `ruff check src`: 7 errores, ninguno nuevo.
- `diff` de snapshots (lógica y menú) vacío.

## Decisions
- Helpers privados (`_`) en el mismo módulo: no amplía API pública ni crea módulos nuevos (imports planos, tests dependen de `gestor`).
- `_descuento_volumen` devuelve `0` int cuando no aplica para que `venta["descuento"]` siga siendo `0` (no `0.0`) en el dict/JSON.
- Ticket condiciona por `venta["descuento"] > 0` en vez de `desc > 0`: equivalente porque un descuento no nulo es siempre ≥ $4 (2% de >200) o ≥ $25 (5% de 500), nunca se redondea a 0.
- VIP solo en `registrar_venta`: `cotizar` hoy no lo aplica; igualarlos cambiaría comportamiento (anotado como posible bug para otro plan).
- `resumen_ventas` con `total_vendido()`: `round(round(t,2),2) == round(t,2)`, salida idéntica.
- Dispatch dict en `menu`: baja complejidad sin cambiar textos ni flujo; "8" queda explícito por el `break`.

## Bitácora (borrador fila #3)
- Prompt: "Extraer funciones de código duplicado o bloques muy largos"
- Cambio: `registrar_venta` partida en `_validar_venta`/`_descuento_volumen`/`_es_vip`/`_armar_ticket` (descuento compartido con `cotizar`); `menu` despachado por funciones por opción; `reportes` reusa `total_vendido` y `_stock_bajo`. Plan: [specs/extraer-funciones.md](specs/extraer-funciones.md)
- Justificación: elimina Long Method y Duplicated Code; ruff C901×2, SIM102×3, SIM108.
- Tests OK: `✅ 20 passed` + conteo ruff real (esperado 7).

## Verification
`pytest && ruff check src --statistics`; diff de snapshots antes/después (lógica con fecha fija + menú vía `printf ... | python <repo>/src/main.py` desde scratchpad); `ruff check src --select C901` sin hallazgos.
