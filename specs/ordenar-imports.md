# Ordenar imports en main.py

## Scope
Solo `src/main.py`: reordenar el bloque de imports (`almacen`, `gestor`, `reportes`) para quitar ruff I001. Sin cambios de lógica.

## Scores genéricos
- Riesgo: 1/5
- Impacto legibilidad/mantenibilidad: 1/5
- Esfuerzo: 1/5
- Errores ruff: 1 → 0

## Implementation plan
1. `git checkout -b refactor/ordenar-imports`.
2. Reordenar imports alfabéticamente (`ruff check src --fix`).
3. `pytest` + `ruff check src`.
4. Fila #7 en `BITACORA.md`, commit atómico y push.

## Acceptance criteria
- `ruff check src`: 0 errores.
- `pytest`: 20 passed, tests intactos.

## Decisions
- Se usa el autofix de ruff: el cambio es trivial y determinista.

## Bitácora (borrador fila #7)
- Prompt: "Reparar el import"
- Cambio: imports de `main.py` en orden alfabético. Plan: [specs/ordenar-imports.md](specs/ordenar-imports.md)
- Justificación: ruff I001 (isort), imports sin ordenar.
- Tests: `✅ 20 passed; ruff 0 errores (antes 1)`
