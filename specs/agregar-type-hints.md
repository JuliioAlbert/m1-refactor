# Agregar type hints a funciones

## Context
Ninguna función de `src/` tiene anotaciones de tipos: no se sabe qué reciben/regresan (`registrar_venta` devuelve dict o `None`, `cotizar` float o `None`, productos/ventas son dicts sin forma declarada). Agregar type hints documenta el contrato, habilita autocompletado/chequeo estático y no cambia comportamiento (Python no valida hints en runtime). Al implementar, este plan se guarda como `specs/agregar-type-hints.md`.

## Scope
Solo `src/` (4 archivos). Nada en `tests/` ni `pyproject.toml`. Sin cambios de lógica, nombres ni mensajes.

- `src/gestor.py`: definir `Producto` y `Venta` como `TypedDict` (claves actuales: producto `codigo, nombre, precio, stock`; venta `folio, codigo, nombre, cantidad, subtotal, descuento, impuesto, total, cliente, fecha, ticket`). Anotar estado global (`INVENTARIO: dict[str, Producto]`, `VENTAS: list[Venta]`, `contadorVentas: int`, `ultimo_error: str`) y funciones:
  - `reiniciar_sistema() -> None`
  - `agregarProducto(codigo: str | None, nombre: str, precio: float, stock: int) -> bool`
  - `eliminar_producto(codigo: str) -> bool`, `actualizar_stock(codigo: str, cantidad: int) -> bool`
  - `buscarProducto(texto: str) -> list[Producto]`
  - `registrar_venta(codigo: str | None, cantidad: int | None, cliente: str | None = "") -> Venta | None`
  - `cotizar(codigo: str, cantidad: int | None) -> float | None`
  - Variables locales solo donde el checker lo necesite (`desc: float = 0`).
- `src/almacen.py`: `guardar_datos(ruta: str) -> bool`, `cargar_datos(ruta: str) -> bool`, `hayArchivo(ruta: str) -> bool`.
- `src/reportes.py`: `hacer_cosa(v: float) -> str`, `productos_stock_bajo() -> list[gestor.Producto]`, `reporte_inventario() -> str`, `total_vendido() -> float`, `mas_vendidos(n: int = 3) -> list[tuple[str, int]]`, `resumen_ventas() -> str`.
- `src/main.py`: `pedir_numero(mensaje: str) -> float`, `menu() -> None`.

Fuera de alcance: renombrar `hacer_cosa`/`hayArchivo`/`contadorVentas`, `with open`, partir `registrar_venta`/`menu`, burbuja → `sorted` (otros planes).

## Scores genéricos
- Riesgo: 1/5 (anotaciones no se ejecutan; único riesgo = import nuevo `typing`)
- Impacto en legibilidad/mantenibilidad: 4/5
- Esfuerzo: 2/5
- Errores ruff: 13 → 13 (no debe subir; ningún ANN seleccionado)

## Implementation plan
1. `git checkout -b refactor/agregar-type-hints` desde `main`.
2. Crear `specs/agregar-type-hints.md` con este plan.
3. Anotar `gestor.py` (TypedDicts + globals + funciones), luego `almacen.py`, `reportes.py`, `main.py`. Sintaxis Py3.10 (`X | None`, `list[...]`) para cumplir UP.
4. `pytest` y `ruff check src` (y opcional `python -m mypy src` si está instalado, solo informativo; no se agrega a requirements).
5. Llenar fila #2 de `BITACORA.md`.
6. Commit atómico `refactor: agregar type hints a funciones de src/` (src + spec + bitácora) con trailer Co-Authored-By; `git push -u origin refactor/agregar-type-hints`.

## Acceptance criteria
- Todas las funciones de `src/` con parámetros y retorno anotados.
- `pytest`: 20 passed, tests sin tocar.
- `ruff check src`: ≤ 13 errores, ninguno nuevo.
- App arranca y sale con opción 8 igual que antes.

## Decisions
- `TypedDict` en vez de `dict[str, Any]`: documenta las claves exactas sin cambiar runtime (sigue siendo dict; JSON cargado y tests compatibles). Vive en `gestor.py`, dueño del estado.
- `| None` solo donde el código ya maneja `None` explícitamente (`codigo`, `cantidad`, `cliente`) para reflejar el contrato real.
- `precio: float` (acepta int por promoción numérica); `cantidad`/`stock: int` (main los convierte con `int()`).
- `ruta: str` (tests pasan `str(tmp_path / ...)`); no se amplía a `PathLike`.

## Bitácora (borrador fila #2)
- Prompt: "Agregar type hints a funciones"
- Cambio: Type hints en todas las funciones de `src/` + `TypedDict` `Producto`/`Venta` y globals anotados. Plan: [specs/agregar-type-hints.md](specs/agregar-type-hints.md)
- Justificación: Contratos implícitos (dicts sin forma, retornos `X | None`) quedan explícitos; habilita chequeo estático y autocompletado. Sin cambio de comportamiento.
- Tests OK: `✅ 20 passed` + conteo ruff real.

## Verification
`pytest && ruff check src --statistics`; `grep -nE "^def .*\)\s*:" src/*.py` vacío (toda def con `->`); smoke test desde scratchpad: `printf '8\n' | python <repo>/src/main.py`.
