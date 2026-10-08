# Renombrar variables y funciones para mayor claridad

## Context
Tras planes 1–5 quedan nombres crípticos/genéricos en `src/` (`x`, `aux`, `temp`, `temp2`, `d`, `s`, `t`, `c`, `cant`, `cli`, `op`, `hacer_cosa`) y 2 violaciones de naming PEP 8 de ruff: N802 `almacen.hayArchivo`, N816 `gestor.contadorVentas`. Meta: nombres que expliquen intención, ruff 3 → 1 error, comportamiento idéntico.

Tests no referencian `contadorVentas`, `hayArchivo`, `hacer_cosa` (verificado con grep) → renombrables. `agregarProducto`/`buscarProducto` se conservan (regla del reto).

## Scope
Solo `src/`. Nada en `tests/`, `pyproject.toml`. Sin cambiar lógica, bubble sort, concatenación de strings ni I001.

**gestor.py**
- `contadorVentas` → `contador_ventas` (global, `reiniciar_sistema`, `registrar_venta`) — quita N816.
- `agregarProducto`: `x` → `producto`.
- `actualizar_stock`: `aux` → `nuevo_stock`.
- `buscarProducto`: `temp2` → `encontrados`; `for k in INVENTARIO` → `for producto in INVENTARIO.values()` (mismo orden).
- `_descuento_vip(subtotal, desc, cliente)`: `desc` → `descuento_previo`.
- `_armar_ticket`: `t` → `ticket`.
- `registrar_venta`: `desc` → `descuento`, `base` → `base_gravable`; `cotizar`: `base` → `base_gravable`.
- Nueva constante `TASA_IVA = 0.16` (junto a reglas de negocio), usada en `registrar_venta` y `cotizar` (misma multiplicación → mismo float).

**almacen.py**
- `hayArchivo` → `existe_archivo` (quita N802); comentario → docstring.
- `d` → `datos` (`guardar_datos`, `_tiene_forma_valida`, `cargar_datos`); `f` → `archivo`; loops `k`/`v` → `codigo`/`venta`.
- `gestor.contadorVentas` → `gestor.contador_ventas`. Clave JSON `"contador"` NO cambia (formato persistido observable).
- `_FALLO` → `_LECTURA_FALLIDA`.

**reportes.py**
- `hacer_cosa(v)` → `formato_dinero(monto)`; comentario → docstring.
- `_stock_bajo(p)`: `p` → `producto`; `productos_stock_bajo`: idem en comprehension.
- `reporte_inventario`: `s` → `reporte`, `aux` → `valor_total`, `k`/`p` → iterar `.values()` como `producto`.
- `total_vendido`: `t` → `total`, `v` → `venta`.
- `mas_vendidos`: `aux` → `unidades_por_codigo`, `temp` → `ranking`, `t` (swap) → tupla-swap `ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]`. Parámetro público `n` se conserva (callers posicionales/keyword).
- `resumen_ventas`: `s` → `resumen`, `v` → `venta`.

**main.py**
- `ARCHIVO` → `ARCHIVO_DATOS`.
- `pedir_numero`: `temp2` → `entrada`.
- `_opcion_agregar_producto`: `c,n,p,s` → `codigo, nombre, precio, stock`.
- `_opcion_registrar_venta`: `c, cant, cli, v` → `codigo, cantidad, cliente, venta`.
- `_opcion_cotizar`: `c, cant, t` → `codigo, cantidad, total`.
- `_opcion_mas_vendidos`: `par` → `for codigo, unidades in ...`.
- `_opcion_stock_bajo`: `bajos` → `productos_bajos`, `p` → `producto`.
- `menu`: `op` → `opcion`; `almacen.hayArchivo` → `almacen.existe_archivo`.

## Scores genéricos
- Riesgo: 1/5 (renombres locales; únicos públicos sin uso en tests)
- Impacto legibilidad/mantenibilidad: 4/5
- Esfuerzo: 1/5
- Errores ruff: 3 → 1 (quedan solo I001)

## Implementation plan
1. `git checkout main && git pull`; `git checkout -b refactor/renombrar-variables`.
2. Snapshot "antes" en scratchpad (mismo método que planes previos): API (ventas normal/500/1000/VIP, cotizaciones, errores + `ultimo_error`, reportes, `mas_vendidos`, stock bajo, guardar/cargar con JSON resultante) y menú vía `printf` (opciones 1–8, inválida, con/sin `datos_ejemplo.json`) → `antes.txt`, `menu_antes.txt`. Script de snapshot debe leer folio vía API/JSON, no `contadorVentas`.
3. Copiar este plan a `specs/renombrar-variables.md`.
4. `gestor.py` → `pytest` + `ruff check src`.
5. `almacen.py` → idem.
6. `reportes.py` → idem.
7. `main.py` → idem.
8. `grep -rnE "contadorVentas|hayArchivo|hacer_cosa" src` vacío.
9. Snapshot "después" → `diff` vacío.
10. Fila #6 en `BITACORA.md`.
11. Commit atómico `refactor: renombrar variables y funciones para mayor claridad` (src + spec + bitácora, trailer Co-Authored-By) → `git push -u origin refactor/renombrar-variables`.

## Acceptance criteria
- Sin nombres de una letra/genéricos (`x`, `aux`, `temp*`, `d`, `s`, `t`, `c`, `cant`, `cli`, `op`, `par`) fuera de índices `i`/`j` del sort.
- Sin `contadorVentas`, `hayArchivo`, `hacer_cosa` en `src/`.
- `0.16` solo como `TASA_IVA`.
- Clave JSON `"contador"` intacta; snapshots antes/después idénticos.
- `pytest`: 20 passed, tests intactos. `ruff check src`: 1 error (I001), ninguno nuevo.

## Decisions
- Parámetros de funciones públicas no se renombran (posibles llamadas con keyword).
- `agregarProducto`/`buscarProducto` intactos (regla del reto, `ignore-names`).
- `existe_archivo` / `formato_dinero` / `contador_ventas`: snake_case en español, consistente con el resto.
- `TASA_IVA` incluido: es dar nombre a un literal, en línea con "claridad".
- I001 (orden de imports en `main.py`) fuera de alcance → plan aparte (último error ruff).
- Bubble sort se mantiene (solo renombre + swap por tupla, mismo algoritmo y estabilidad).

## Bitácora (borrador fila #6)
- Prompt: "Renombrar variables o funciones para mayor claridad"
- Cambio: nombres descriptivos en `src/` (`hacer_cosa`→`formato_dinero`, `hayArchivo`→`existe_archivo`, `contadorVentas`→`contador_ventas`, `aux/temp/d/s/t`→nombres de intención, `TASA_IVA`). Plan: [specs/renombrar-variables.md](specs/renombrar-variables.md)
- Justificación: elimina Poor Naming / Mysterious Name; quita ruff N802 y N816.
- Tests: `✅ 20 passed; ruff 1 error (antes 3)` (real tras correr).

## Resultado
- `pytest`: 20 passed. `ruff check src`: 1 error (I001). Snapshots antes/después idénticos (API, ignorando `fecha`; menú con y sin `datos_ejemplo.json`).
- Ajustes menores: líneas partidas para respetar E501 (88) en `reportes.py` y `main.py`.

## Verification
- `pytest` → 20 passed; `ruff check src` → solo I001.
- `diff antes.txt despues.txt`, `diff menu_antes.txt menu_despues.txt` vacíos.
- `cd src && printf '4\n8\n' | python main.py` corre sin error.
