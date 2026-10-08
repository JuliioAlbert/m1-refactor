# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Reto de refactorización: app de consola en Python (inventario y ventas, tienda "La Esquina"). Funciona y los tests pasan, pero `src/` tiene code smells a propósito; la misión es mejorarlo sin cambiar el comportamiento observable. Código, comentarios y mensajes al usuario están en español; mantenlo.

## Commands

- Install: `pip install -r requirements.txt` (pytest, ruff; Python >= 3.10)
- Tests: `pytest`; one test: `pytest tests/test_gestor.py::<nombre_del_test>`
- Lint: `ruff check src` (meta final: 0 errores; `--fix` solo arregla lo trivial). Tests no se lintean.
- Run app: `cd src && python main.py` (carga `datos_ejemplo.json` relativo al cwd, así que desde `src/` no lo encuentra salvo que exista ahí)

## Reglas del reto

- NO modificar `tests/` ni `pyproject.toml` (config de ruff: C90 max-complexity 10, naming PEP 8, SIM, UP, etc.).
- Comportamiento observable idéntico; los tests son de caja negra. Correr `pytest` y `ruff check src` tras CADA refactorización.
- `agregarProducto` y `buscarProducto` conservan su nombre (los tests los usan; están en `ignore-names`).
- Entrega: rama `refactorizacion` → PR a `main`, commits atómicos (uno por refactorización), `BITACORA.md` (copia de `BITACORA_TEMPLATE.md`) con prompt/cambio/justificación/resultado de tests por refactorización + reflexión. Mínimo 5 refactorizaciones significativas.
- `.claudeignore` es parte de la entrega (excluye venvs, cachés, datos generados).

## Planes

Guardar todos los planes como archivos Markdown en `/specs` (raíz del repo; crear la carpeta si no existe), uno por plan, nombre en kebab-case (ej. `specs/extraer-descuentos.md`). Cada plan debe contener estas secciones, en este orden:

1. Scope
2. Scores genéricos
3. Implementation plan
4. Acceptance criteria
5. Decisions

Al aplicar un plan, crear primero una rama nueva de git (ej. `refactor/<nombre-del-plan>`, mismo nombre que el archivo en `specs/`), guardar ahí los cambios con commits y publicarla en GitHub (`git push -u origin <rama>`). Nunca commitear directo a `main`.



Antes de entregar, fusionar todas las ramas de plan en `refactorizacion` (`git merge`) y abrir el PR `refactorizacion` → `main`.

## Architecture

Módulos planos en `src/` (imports sin paquete: `import gestor`; `tests/conftest.py` agrega `src/` al `sys.path`).

- `gestor.py`: lógica de negocio. Estado global a nivel de módulo: `INVENTARIO` (dict codigo→producto), `VENTAS` (list), `contadorVentas` (folio), `ultimo_error` (motivo del último fallo). Las funciones devuelven `False`/`None` en error y dejan el motivo en `ultimo_error` (no lanzan excepciones). `registrar_venta` mezcla validación, descuentos, IVA, stock, folio y ticket; `cotizar` duplica la lógica de descuento/IVA.
- `almacen.py`: persistencia JSON. Lee/escribe directamente `gestor.INVENTARIO`, `gestor.VENTAS`, `gestor.contadorVentas` y `gestor.ultimo_error`; por eso mutar esos objetos (`.clear()`, asignación vía `gestor.x = ...`) importa: otros módulos y tests mantienen referencias a ellos.
- `reportes.py`: reportes de inventario/ventas/más vendidos; lee el estado de `gestor`.
- `main.py`: menú interactivo; orquesta `gestor`, `almacen`, `reportes`.
- `tests/conftest.py`: fixture autouse que llama `gestor.reiniciar_sistema()` antes y después de cada test, así que el estado global debe seguir reiniciable por esa función.

Reglas de negocio a preservar: descuento por volumen (>=1000 → 10%, >=500 → 5%), extra 2% del subtotal para clientes con prefijo `VIP` si subtotal-descuento > 200, IVA 16%, totales redondeados a 2 decimales, formato exacto del ticket.
