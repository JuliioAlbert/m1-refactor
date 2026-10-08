# Reto: Refactorización Asistida por IA

## Gestor de inventario y ventas — Tienda "La Esquina"

Este repositorio contiene una aplicación de consola en Python para administrar
el inventario y las ventas de una tienda pequeña: alta de productos, registro
de ventas con descuentos e IVA, cotizaciones, alertas de stock bajo, reporte de
más vendidos y persistencia de datos en JSON.

**El programa funciona correctamente** (todas las pruebas pasan), pero el código
fue escrito "al aventón" y arrastra una cantidad importante de malas prácticas:
funciones gigantes que hacen de todo, lógica duplicada, nombres crípticos,
números mágicos, estado global, código muerto, anidamiento excesivo, estilos de
nombrado mezclados... Tu misión es **mejorarlo sin romperlo**, usando Claude
Code como asistente.

### Estructura del proyecto

```
.
├── CLAUDE.md            # Instrucciones para Claude Code
├── .claudeignore        # Archivos que Claude Code ignora
├── README.md            # Documentación del proyecto
├── requirements.txt     # Dependencias
├── pyproject.toml       # Configuración del linter (ruff) — NO la modifiques
├── datos_ejemplo.json   # Datos de ejemplo para el menú interactivo
├── BITACORA_TEMPLATE.md # Plantilla original de la bitácora
├── src/
│   ├── gestor.py        # Lógica de productos y ventas
│   ├── almacen.py       # Carga y guardado de datos (JSON)
│   ├── reportes.py      # Reportes e indicadores
│   └── main.py          # Menú interactivo de consola
├── tests/               # Suite de pruebas (pytest) — NO la modifiques
├── specs/               # Plan de cada refactorización
└── docs/
    ├── bitacora.md      # Registro de cada refactorización
    └── reflexion.md     # Aprendizajes y conclusiones
```

## Instalación y ejecución

### Requisitos previos

- **Python 3.10 o superior** (verificado con 3.11 y 3.14).
- **pip** y **git**.
- Dependencias (`requirements.txt`): `pytest>=8.0` y `ruff>=0.6` (verificado con pytest 9.1.1 y ruff 0.16.10).

### Clonar e instalar

```bash
# 1. Clonar el repositorio
git clone https://github.com/JuliioAlbert/m1-refactor.git
cd m1-refactor

# 2. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar los tests

```bash
pytest          # o `pytest -v` para ver cada test
```

### Ejecutar el linter

```bash
ruff check src             # debe reportar 0 errores
ruff format --check src    # debe reportar 0 archivos por reformatear
```

### Ejecutar la aplicación (opcional)

```bash
cd src && python main.py
```

### Evidencia de tests pasando

Salida real (2026-10-07, rama `refactor/aplicar-ruff-format`):

```text
$ pytest -v
collected 20 items

tests/test_almacen.py::test_guardar_y_cargar_conserva_los_datos PASSED   [  5%]
tests/test_almacen.py::test_el_folio_continua_despues_de_recargar PASSED [ 10%]
tests/test_almacen.py::test_cargar_archivo_inexistente_regresa_false PASSED [ 15%]
tests/test_gestor.py::test_agregar_producto_queda_en_inventario PASSED   [ 20%]
tests/test_gestor.py::test_rechaza_altas_invalidas PASSED                [ 25%]
tests/test_gestor.py::test_actualizar_stock_suma_y_resta PASSED          [ 30%]
tests/test_gestor.py::test_eliminar_producto PASSED                      [ 35%]
tests/test_gestor.py::test_buscar_producto_por_nombre PASSED             [ 40%]
tests/test_gestor.py::test_venta_descuenta_stock_y_asigna_folio PASSED   [ 45%]
tests/test_gestor.py::test_venta_sin_descuento_aplica_iva PASSED         [ 50%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_medio PASSED  [ 55%]
tests/test_gestor.py::test_venta_con_descuento_por_volumen_alto PASSED   [ 60%]
tests/test_gestor.py::test_venta_cliente_vip_recibe_descuento_extra PASSED [ 65%]
tests/test_gestor.py::test_venta_rechaza_stock_insuficiente PASSED       [ 70%]
tests/test_gestor.py::test_venta_rechaza_producto_inexistente_y_cantidad_invalida PASSED [ 75%]
tests/test_gestor.py::test_cotizar_coincide_con_el_total_de_la_venta PASSED [ 80%]
tests/test_reportes.py::test_stock_bajo_detecta_los_correctos PASSED     [ 85%]
tests/test_reportes.py::test_total_vendido_suma_las_ventas PASSED        [ 90%]
tests/test_reportes.py::test_mas_vendidos_ordena_por_unidades PASSED     [ 95%]
tests/test_reportes.py::test_reporte_inventario_marca_stock_bajo PASSED  [100%]

============================== 20 passed in 0.02s ==============================

$ ruff check src
All checks passed!

$ ruff format --check src
4 files already formatted
```

## Instrucciones del reto

Trabaja en un **fork** de este repositorio y sigue estos pasos:

1. **Configura el proyecto para Claude Code.** Crea un `CLAUDE.md` con el
   contexto del proyecto (qué hace, cómo correr las pruebas, reglas que la IA
   debe respetar — por ejemplo, *no modificar los tests*) y un `.claudeignore`
   con lo que no debe leer (entornos virtuales, cachés, datos generados).
   Crear estos archivos es parte del reto: **no vienen incluidos**.
2. **Explora el código con Claude Code.** Pídele un diagnóstico: qué *code
   smells* detecta y qué refactorizaciones recomienda. Prioriza.
3. **Aplica al menos 5 refactorizaciones significativas**, una a la vez.
   Ejemplos válidos: dividir una función gigante, extraer lógica duplicada,
   renombrar con nombres descriptivos y estilo consistente, reemplazar números
   mágicos por constantes, aplanar condicionales anidados, eliminar código
   muerto, agregar type hints, reducir el estado global, separar lógica de
   entrada/salida. Cambios cosméticos aislados (una línea, un espacio) no
   cuentan como refactorización significativa.
4. **Valida con `pytest` y `ruff check src` después de CADA refactorización.** La suite de
   pruebas es de caja negra: si un cambio la rompe, tu refactorización alteró
   el comportamiento y debes corregirla. **No está permitido modificar los
   tests** para hacerlos pasar.
5. **Documenta cada prompt en la bitácora.** Copia `BITACORA_TEMPLATE.md` a
   `docs/bitacora.md` y llena una fila por refactorización: prompt usado, cambio
   realizado, justificación y resultado de los tests. Cierra con tu reflexión.
6. **Entrega mediante Pull Request** hacia tu propio repositorio (rama
   `refactorizacion` → `main`), con commits atómicos (idealmente uno por
   refactorización) y la bitácora incluida. Comparte la liga del PR en la
   plataforma del curso.

## Criterios de evaluación

| Criterio | Descripción | Peso |
|----------|-------------|------|
| Configuración | `CLAUDE.md` y `.claudeignore` completos y pertinentes | 15% |
| Calidad de refactorizaciones | ≥5 refactorizaciones significativas, bien elegidas y bien ejecutadas | 30% |
| Tests pasando | La suite completa pasa al final (y después de cada cambio) | 20% |
| Bitácora | Prompts documentados, cambios explicados y justificados | 25% |
| Reflexión | Análisis crítico del trabajo con la IA | 10% |

## Reglas

- No modifiques los archivos de `tests/` ni `pyproject.toml`.
- El código final de `src/` debe pasar `ruff check src` **sin errores**. La
  configuración ya viene incluida en `pyproject.toml`; cada regla corresponde a
  un *code smell* real del proyecto (funciones demasiado complejas, nombres que
  no siguen PEP 8, archivos abiertos sin `with`, imports sin usar, `if`
  anidados…). `ruff check src --fix` corrige solo los triviales: el resto es
  trabajo de refactorización. Las funciones `agregarProducto` y
  `buscarProducto` conservan su nombre porque los tests las usan.
- El comportamiento observable del programa debe mantenerse idéntico.
- Puedes (y debes) usar Claude Code, pero **tú eres responsable** de revisar,
  entender y validar cada cambio que la IA proponga.
