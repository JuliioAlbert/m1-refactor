# Aplicar ruff format

## Scope
`src/gestor.py` y `src/main.py`: aplicar `ruff format` (solo whitespace/saltos de línea). Además documentar el comando en `CLAUDE.md` y completar `README.md` (requisitos, instalación, tests, linter, evidencia).

## Scores genéricos
- Riesgo: 1/5
- Impacto legibilidad/mantenibilidad: 2/5
- Esfuerzo: 1/5
- Archivos sin formato: 2 → 0

## Implementation plan
1. `git checkout -b refactor/aplicar-ruff-format`.
2. `ruff format src`.
3. Agregar `ruff format --check src` a `CLAUDE.md`.
4. Reescribir sección de instalación del `README.md` con evidencia.
5. `pytest` + `ruff check src` + `ruff format --check src`.
6. Fila #8 en `BITACORA.md`, commit atómico y push.

## Acceptance criteria
- `ruff check src`: 0 errores.
- `ruff format --check src`: 0 archivos por reformatear.
- `pytest`: 20 passed, tests intactos.
- README con requisitos, instalación, comandos de tests y linter, evidencia.

## Decisions
- Se usa el formateador de ruff con la config existente (`line-length = 88`); `pyproject.toml` no se toca.

## Bitácora (borrador fila #8)
- Prompt: "Aplicar a que pase el linter configurar en el md"
- Cambio: `ruff format src` + README/CLAUDE.md actualizados. Plan: [specs/aplicar-ruff-format.md](specs/aplicar-ruff-format.md)
- Justificación: formato consistente (PEP 8 / ruff format); documentación de entrega.
- Tests: `✅ 20 passed; ruff 0 errores; format 0 pendientes (antes 2)`
