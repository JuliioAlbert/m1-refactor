# Mejorar manejo de errores

## Context
Manejo de errores frágil en `src/`:
- `almacen.guardar_datos`/`cargar_datos` usan `open` sin context manager (SIM115 ×2, UP015): si `json.dump/load` lanza, el archivo queda abierto. `guardar_datos` siempre regresa `True`; un `OSError` revienta la app.
- `cargar_datos` usa `except Exception` (traga todo) y, tras parsear, accede `d["inventario"]`/`d["ventas"]` sin validar: JSON válido pero con otra forma → `KeyError`/`TypeError` y estado a medias (inventario reemplazado, ventas no).
- `main.menu` ignora los retornos: imprime "Datos cargados de…" aunque la carga falle y "Datos guardados." aunque no se guarde.
- `main` hace `int(pedir_numero(...))`: "inf"/"nan" → `OverflowError`/`ValueError` (traceback); "1.5" se trunca a 1 en silencio. `pedir_numero` acepta "inf" como precio (JSON no estándar `Infinity`).
- Mensajes de error como literales duplicados en `gestor.py` ("producto no existe" ×4, "codigo vacio" ×2, "cantidad invalida" ×2).

Alcance elegido por el usuario: estructural + caminos de falla. Caminos felices, contrato `False`/`None` + `ultimo_error` y los 20 tests quedan idénticos. Al implementar, este plan se guarda como `specs/mejorar-manejo-de-errores.md`.

## Scope
Solo `src/gestor.py`, `src/almacen.py`, `src/main.py`. Nada en `tests/`, `pyproject.toml`, `reportes.py`. Sin excepciones nuevas hacia el llamador (tests esperan `is False`/`is None`).

**gestor.py**
- Constantes de módulo para los motivos: `ERROR_CODIGO_VACIO = "codigo vacio"`, `ERROR_NO_EXISTE = "producto no existe"`, `ERROR_YA_EXISTE`, `ERROR_PRECIO`, `ERROR_STOCK`, `ERROR_STOCK_NEGATIVO`, `ERROR_CANTIDAD`, `ERROR_STOCK_INSUFICIENTE`. Mismos textos exactos; usarlas en `agregarProducto`, `eliminar_producto`, `actualizar_stock`, `_validar_venta`, `cotizar`.

**almacen.py**
- `guardar_datos`: `try: with open(...) as f: json.dump(...)` / `except OSError:` → `gestor.ultimo_error = "no se pudo guardar el archivo"`, `return False`.
- `cargar_datos`: EAFP en helper `_leer_json(ruta) -> dict | None`:
  - `with open(ruta, encoding="utf-8")` (sin `"r"`, UP015).
  - `FileNotFoundError` → "el archivo no existe" (mismo texto que hoy; reemplaza `os.path.exists` previo).
  - `json.JSONDecodeError`, `UnicodeDecodeError` → "archivo corrupto".
  - otro `OSError` (permiso, directorio) → "no se pudo leer el archivo".
- Validar forma **antes** de mutar estado: `dict` con `"inventario"` dict y `"ventas"` list; si no → "archivo corrupto", `False`, estado intacto.
- `hayArchivo` sin cambios (renombrar es otro plan; SIM103 fuera de alcance).

**main.py**
- `pedir_numero`: además rechaza no finitos (`math.isfinite`) con el mismo mensaje "Eso no es un numero, intenta de nuevo.".
- Nuevo `pedir_entero(mensaje) -> int`: usa `pedir_numero`; si no `is_integer()` → "Debe ser un numero entero, intenta de nuevo." y repite. "2" y "2.0" siguen dando 2. Usar en stock, cantidad de venta y cotización.
- `menu`: si `hayArchivo`, `if almacen.cargar_datos(ARCHIVO): print("Datos cargados de", ARCHIVO)` / `else: _mostrar_error()`.
- Opción 8: `if almacen.guardar_datos(ARCHIVO): print("Datos guardados. Hasta luego.")` / `else: _mostrar_error()`; sale en ambos casos (`break`).

Fuera de alcance: convertir a excepciones propias, renombres (`hayArchivo`, `contadorVentas`), I001, SIM103, Ctrl+C/EOF, validar `nombre` vacío.

## Scores genéricos
- Riesgo: 2/5 (cambia solo caminos de falla; caminos felices verificados con snapshot)
- Impacto en robustez/mantenibilidad: 4/5
- Esfuerzo: 2/5
- Errores ruff: 7 → 4 (desaparecen SIM115 ×2, UP015)

## Implementation plan
1. `git checkout main && git pull && git checkout -b refactor/mejorar-manejo-de-errores`.
2. Snapshot "antes" en scratchpad (mismo método que `specs/extraer-funciones.md`): ventas normal/medio/alto/VIP con fecha fija, cotizaciones, reportes, errores de `gestor` + `ultimo_error`, guardar/cargar ida y vuelta; menú vía `printf` (opciones 1–8 + inválida, cwd = scratchpad) → `antes.txt`, `menu_antes.txt`.
3. Crear `specs/mejorar-manejo-de-errores.md` con este plan (secciones en orden de CLAUDE.md + Bitácora).
4. `gestor.py` constantes → `pytest` + `ruff check src`.
5. `almacen.py` → `pytest` + `ruff`.
6. `main.py` → `pytest` + `ruff`.
7. Snapshot "después" → `diff` vacío. Script de casos de falla (ver Verification).
8. Llenar fila #4 de `BITACORA.md`.
9. Commit atómico `refactor: mejorar manejo de errores` (src + spec + bitácora, trailer Co-Authored-By) → `git push -u origin refactor/mejorar-manejo-de-errores`.

## Acceptance criteria
- Sin `open` fuera de `with`; sin `except Exception` en `src/`.
- `cargar_datos` nunca lanza ante archivo inexistente/corrupto/mal formado/ilegible; regresa `False`, fija `ultimo_error` y no modifica `INVENTARIO`/`VENTAS`/`contadorVentas`.
- `guardar_datos` regresa `False` + `ultimo_error` ante `OSError`.
- `main` no imprime "Datos cargados"/"Datos guardados" si la operación falló; "inf"/"nan"/"1.5" en campos enteros no truenan ni truncan.
- Ningún literal de motivo de error duplicado en `gestor.py`.
- `pytest`: 20 passed, tests intactos. `ruff check src`: 4 errores, ninguno nuevo.
- `diff` de snapshots de caminos felices vacío.

## Decisions
- Mantener contrato sentinela (`False`/`None` + `ultimo_error`) en vez de excepciones: los tests de caja negra lo exigen y `almacen` ya escribe `gestor.ultimo_error`.
- EAFP (`FileNotFoundError`) en lugar de `os.path.exists` + `open`: elimina carrera y reutiliza el mismo mensaje.
- Validar forma antes de mutar: evita estado a medias (antes `ventas` faltante dejaba inventario nuevo con ventas viejas).
- `contador` sigue opcional (`d.get("contador", 0)`), `ventas` sigue obligatorio, como hoy.
- Si guardar falla al salir, se muestra error y se sale igual: flujo de salida idéntico, solo deja de mentir.
- `pedir_entero` acepta "2.0" para no romper entradas que hoy funcionan; solo rechaza fracciones (antes truncadas en silencio).
- Constantes `ERROR_*` públicas en `gestor` para que `almacen` pueda seguir el mismo patrón si se desea; sin cambio de textos.

## Bitácora (borrador fila #4)
- Prompt: "Mejorar manejo de errores" (alcance elegido: estructural + caminos de falla).
- Cambio: `with open` + excepciones acotadas y validación de forma en `almacen`; `main` revisa retornos de cargar/guardar y valida enteros finitos; motivos de error como constantes en `gestor`. Plan: [specs/mejorar-manejo-de-errores.md](specs/mejorar-manejo-de-errores.md)
- Justificación: elimina fuga de archivos, `except Exception` que oculta bugs, estado a medias, mensajes engañosos y tracebacks por entrada; quita ruff SIM115 ×2 y UP015.
- Tests OK: `✅ 20 passed; ruff 4 errores (antes 7)` (llenar con resultado real).

## Verification
- `pytest` → 20 passed; `ruff check src` → 4.
- Snapshot diff vacío (lógica + menú).
- Script en scratchpad (run con `cwd=src` en sys.path): `cargar_datos` con archivo inexistente, `"{"`, `[]`, `{"inventario": {}}`, directorio → `False`, motivo esperado, estado sin cambios; `guardar_datos` a ruta en directorio inexistente → `False`, "no se pudo guardar el archivo".
- Menú: `datos_ejemplo.json` corrupto en scratchpad → imprime "Error: archivo corrupto", no "Datos cargados"; entradas `inf`, `nan`, `1.5`, luego `3` en cantidad → reintenta sin traceback.
