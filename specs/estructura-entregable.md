# Estructura del entregable

## Scope
Mover `BITACORA.md` → `docs/bitacora.md` y `reflexion.md` → `docs/reflexion.md`; actualizar links y referencias en `README.md`/`CLAUDE.md`. Sin cambios en `src/` ni `tests/`.

## Scores genéricos
- Riesgo: 1/5
- Impacto legibilidad/mantenibilidad: 2/5
- Esfuerzo: 1/5
- Errores ruff: 0 → 0

## Implementation plan
1. `git checkout -b refactor/estructura-entregable`.
2. `git mv` de bitácora y reflexión a `docs/`; links `specs/` → `../specs/`.
3. Actualizar árbol del README y rutas en `CLAUDE.md`.
4. `pytest` + `ruff check src` + `ruff format --check src`.
5. Fila #9 en `docs/bitacora.md`, commit atómico y push.

## Acceptance criteria
- `docs/bitacora.md` y `docs/reflexion.md` existen; no quedan en raíz.
- Sin rutas viejas en `README.md`/`CLAUDE.md`.
- `pytest`: 20 passed; ruff 0 errores; format 0 pendientes.

## Decisions
- `pyproject.toml`, `datos_ejemplo.json`, `specs/` y `BITACORA_TEMPLATE.md` se quedan en raíz (config, cwd de la app, regla de planes y plantilla original).

## Bitácora (borrador fila #9)
- Prompt: "puedes generar el entregable con este orden de carpetas"
- Cambio: bitácora y reflexión movidas a `docs/`. Plan: [specs/estructura-entregable.md](../specs/estructura-entregable.md)
- Justificación: estructura de entrega requerida; docs separados del código.
- Tests: `✅ 20 passed; ruff 0 errores; format 0 pendientes`
