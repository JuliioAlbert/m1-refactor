# Simplificar condicionales complejos

## Context
Tras planes 1–4, quedan condicionales verbosos/duplicados o con números mágicos en `src/`:
- `almacen.hayArchivo`: `if exists: return True else: return False` (ruff SIM103).
- `gestor`: `codigo is None or codigo == ""` ×2 (`agregarProducto`, `_validar_venta`); `cantidad is None or cantidad <= 0` ×2 (`_validar_venta`, `cotizar`).
- `gestor._es_vip`: `bool(cliente) and cliente[:3] == "VIP"` (slicing en vez de `startswith`).
- `gestor.registrar_venta`: regla VIP inline con mágicos `200` y `0.02`; `_descuento_volumen` con mágicos `1000/500/0.10/0.05` en cadena if.
- `reportes`: `_stock_bajo` con mágico `5`; `mas_vendidos` acumula con `if k in aux ... else`; `productos_stock_bajo` loop+if+append.
- `main`: `menu` con `if` anidado (hayArchivo → cargar_datos); `_opcion_*` con `if not None ... else` en vez de guard clause; `len(bajos) == 0`.

Meta: condiciones legibles y con nombre, sin duplicados ni mágicos; comportamiento idéntico. 

## Scope
Solo `src/`. Nada en `tests/`, `pyproject.toml`. Sin renombres (`hayArchivo`, `contadorVentas`), sin I001, sin tocar bubble sort / concatenación de strings (otros planes).

**gestor.py**
- Constantes: `DESCUENTOS_VOLUMEN = ((1000, 0.10), (500, 0.05))`, `MONTO_MINIMO_VIP = 200`, `DESCUENTO_VIP = 0.02`, `PREFIJO_VIP = "VIP"`.
- `if not codigo:` en lugar de `codigo is None or codigo == ""` (equivalente para `str | None`).
- Helper `_cantidad_invalida(cantidad) -> bool` (`cantidad is None or cantidad <= 0`), usado en `_validar_venta` y `cotizar`.
- `_descuento_volumen`: loop sobre `DESCUENTOS_VOLUMEN`, primer tramo que cumple `subtotal >= minimo` → `subtotal * tasa`; si ninguno `return 0` (mantener int 0, igual que hoy).
- `_es_vip`: `return bool(cliente) and cliente.startswith(PREFIJO_VIP)`.
- Helper `_descuento_vip(subtotal, desc, cliente) -> float`: `subtotal * DESCUENTO_VIP` si `_es_vip(cliente) and subtotal - desc > MONTO_MINIMO_VIP`, si no `0`. En `registrar_venta`: `desc = desc + _descuento_vip(...)` (misma suma, mismo orden → mismo float).

**almacen.py**
- `hayArchivo`: `return os.path.exists(ruta)` (quita SIM103).

**reportes.py**
- `STOCK_MINIMO = 5`; `_stock_bajo` lo usa.
- `productos_stock_bajo`: list comprehension `[p for p in gestor.INVENTARIO.values() if _stock_bajo(p)]` (mismo orden).
- `mas_vendidos`: `aux[c] = aux.get(c, 0) + v["cantidad"]` (orden de inserción igual → mismo resultado del sort estable).

**main.py**
- `_cargar_datos_iniciales()` con guard clause: `if not almacen.hayArchivo(ARCHIVO): return`; luego cargar → mensaje o `_mostrar_error()`. `menu` lo llama.
- `_opcion_registrar_venta`, `_opcion_cotizar`, `_opcion_agregar_producto`: guard clause (`if ... is None: _mostrar_error(); return`).
- `_opcion_stock_bajo`: `if not bajos:` + guard/return.
- Loop de `menu`: `accion = ACCIONES.get(op)`; `if accion is None: print(...); continue`; `accion()`.

## Scores genéricos
- Riesgo: 1/5 (transformaciones equivalentes; snapshot lo confirma)
- Impacto legibilidad/mantenibilidad: 3/5
- Esfuerzo: 1/5
- Errores ruff: 4 → 3 (desaparece SIM103)

## Implementation plan
1. `git checkout main && git pull`; rama `refactor/simplificar-condicionales` ya existe local apuntando a main → `git checkout refactor/simplificar-condicionales` (si difiere de main, `git reset` no; recrear con `git checkout -B` solo si no tiene commits propios — hoy no tiene).
2. Snapshot "antes" en scratchpad (mismo método que `specs/mejorar-manejo-de-errores.md`): ventas normal/500/1000/VIP (bajo y sobre 200, cliente `""`/`None`/`"vip"`), cotizaciones, errores + `ultimo_error`, reportes, `mas_vendidos`, `productos_stock_bajo`, guardar/cargar; menú vía `printf` (opciones 1–8, inválida, con y sin `datos_ejemplo.json`) → `antes.txt`, `menu_antes.txt`.
3. Crear `specs/simplificar-condicionales.md` (Scope, Scores genéricos, Implementation plan, Acceptance criteria, Decisions, Bitácora).
4. `gestor.py` → `pytest` + `ruff check src`.
5. `almacen.py` → `pytest` + `ruff`.
6. `reportes.py` → `pytest` + `ruff`.
7. `main.py` → `pytest` + `ruff`.
8. Snapshot "después" → `diff` vacío.
9. Fila #5 de `BITACORA.md`.
10. Commit atómico `refactor: simplificar condicionales complejos` (src + spec + bitácora, trailer Co-Authored-By) → `git push -u origin refactor/simplificar-condicionales`.

## Acceptance criteria
- Sin `codigo is None or codigo == ""`, sin `cantidad is None or cantidad <= 0` duplicado, sin `[:3] == "VIP"`, sin `if ...: return True else: return False`.
- Sin literales mágicos `200`, `0.02`, `1000`, `500`, `0.10`, `0.05`, `5` en condiciones (todas como constantes con nombre).
- Sin `if` anidado en `menu`; opciones usan guard clauses.
- Snapshots antes/después idénticos (incluye tickets, `descuento` int 0 vs float).
- `pytest`: 20 passed, tests intactos. `ruff check src`: 3 errores (N802, N816, I001), ninguno nuevo.

## Decisions
- `return 0` en `_descuento_volumen`/`_descuento_vip` se mantiene int (JSON guardado y ticket idénticos).
- `if not codigo` vs `is None or == ""`: equivalentes con anotación `str | None`.
- `hayArchivo` no se renombra (N802 queda para otro plan; tests no lo usan pero main sí).
- Bubble sort de `mas_vendidos` fuera de alcance (no es condicional complejo; plan aparte).
- Reutilizar rama local existente `refactor/simplificar-condicionales`.

## Bitácora (borrador fila #5)
- Prompt: "Simplificar condicionales complejos"
- Cambio: condiciones con nombre (`_cantidad_invalida`, `_descuento_vip`, `startswith`), tramos de descuento y umbrales como constantes, guard clauses en `main`, `hayArchivo` retorna directo. Plan: [specs/simplificar-condicionales.md](specs/simplificar-condicionales.md)
- Justificación: elimina Complex Conditional, Magic Numbers y condiciones duplicadas; quita ruff SIM103.
- Tests: `✅ 20 passed; ruff 3 errores (antes 4)` (real tras correr).

## Resultado
- `pytest`: 20 passed. `ruff check src`: 3 errores (N802, N816, I001). Snapshots antes/después idénticos (API + menú con y sin `datos_ejemplo.json`).

## Verification
- `pytest` → 20 passed; `ruff check src` → 3.
- `diff antes.txt despues.txt` y `diff menu_antes.txt menu_despues.txt` vacíos.
