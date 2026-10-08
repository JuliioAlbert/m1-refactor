# Eliminar código muerto y comentarios obsoletos

## Context
Reto de refactorización: `src/` tiene código muerto y comentarios obsoletos a propósito. Quitarlos reduce ruido y errores de ruff (F401, ERA001, UP009, N802) sin cambiar comportamiento observable. Al implementar, este plan se guarda como `specs/eliminar-codigo-muerto.md` (secciones abajo, en el orden exigido por CLAUDE.md).

## Scope
Solo `src/`. Nada en `tests/` ni `pyproject.toml`. Sin cambios de lógica.

Elementos a eliminar (verificado con grep: ninguno referenciado en `src/` ni `tests/`):
- `src/gestor.py:17` `MODO_DEBUG = False` — nunca leído.
- `src/gestor.py:185-190` `calcular_descuento_viejo` — fórmula 2023, sin llamadas.
- `src/gestor.py:193-198` bloque comentado `exportar_txt` (ERA001).
- `src/reportes.py:4` `import os` sin uso (F401).
- `src/reportes.py:83-92` `reporteViejoCSV` — "ya no se usa", sin llamadas (quita también N802 + SIM115).
- Línea 1 `# -*- coding: utf-8 -*-` en los 4 archivos de `src/` (obsoleto en Py3, UP009).
- `src/gestor.py:4-5` frase del docstring "Historicamente este archivo lo fueron parchando varias personas, asi que hay de todo un poco." — comentario obsoleto/sin valor; queda solo la primera línea del docstring.

Fuera de alcance (otras refactorizaciones): `hayArchivo` (sí se usa en `main.py`), `hacer_cosa` (renombrar), burbuja + su `TODO` en `mas_vendidos`, `temp2`/`aux`, `open` sin `with`.

## Scores genéricos
- Riesgo: 1/5 (solo borrado de código no referenciado)
- Impacto en legibilidad: 3/5
- Esfuerzo: 1/5
- Errores ruff eliminados: ~9 de 20 (F401, 2×ERA001→5 líneas, 4×UP009, N802, SIM115)

## Implementation plan
1. `git checkout -b refactor/eliminar-codigo-muerto` desde `main`.
2. Crear `specs/eliminar-codigo-muerto.md` con este plan.
3. Editar `src/gestor.py`, `src/reportes.py`, `src/almacen.py`, `src/main.py` según Scope.
4. `pytest` y `ruff check src`.
5. Commit atómico: `refactor: eliminar código muerto y comentarios obsoletos` (+ spec), con trailer Co-Authored-By.
6. `git push -u origin refactor/eliminar-codigo-muerto`.

## Acceptance criteria
- `pytest` 100% verde, sin modificar tests.
- `ruff check src` sin F401, ERA001, UP009; N802 baja de 2 a 1; total de errores baja.
- `grep -rnE "MODO_DEBUG|calcular_descuento_viejo|reporteViejoCSV|exportar_txt|coding: utf-8" src` vacío.
- App arranca y sale con opción 8 igual que antes.

## Decisions
- `hayArchivo` se conserva: está en uso; su simplificación es otra refactorización.
- El `TODO` de burbuja se conserva: se resuelve al reemplazar la burbuja por `sorted` (plan aparte).
- Se borran funciones "por si acaso": el historial de git las preserva.

## Verification
`pytest && ruff check src --statistics`; grep de arriba; smoke test desde scratchpad (para no generar `datos_ejemplo.json` en el repo): `printf '8\n' | python <repo>/src/main.py`.
