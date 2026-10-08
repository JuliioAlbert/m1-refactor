"""Persistencia del gestor: carga y guardado de datos en JSON."""

import json
import os
from typing import Any

import gestor

_LECTURA_FALLIDA = object()


def guardar_datos(ruta: str) -> bool:
    """Guarda el inventario, las ventas y el folio actual en un JSON.

    Regresa False si no se puede escribir el archivo.
    """
    datos = {}
    datos["inventario"] = gestor.INVENTARIO
    datos["ventas"] = gestor.VENTAS
    datos["contador"] = gestor.contador_ventas
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
    except OSError:
        gestor.ultimo_error = "no se pudo guardar el archivo"
        return False
    return True


def _leer_json(ruta: str) -> Any:
    """Regresa el contenido del JSON o _LECTURA_FALLIDA (con ultimo_error) si falla."""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        gestor.ultimo_error = "el archivo no existe"
    except (json.JSONDecodeError, UnicodeDecodeError):
        gestor.ultimo_error = "archivo corrupto"
    except OSError:
        gestor.ultimo_error = "no se pudo leer el archivo"
    return _LECTURA_FALLIDA


def _tiene_forma_valida(datos: Any) -> bool:
    return (
        isinstance(datos, dict)
        and isinstance(datos.get("inventario"), dict)
        and isinstance(datos.get("ventas"), list)
    )


def cargar_datos(ruta: str) -> bool:
    """Lee el archivo JSON y deja los datos en el estado global.

    Regresa False si el archivo no existe, esta corrupto o no se puede leer;
    en ese caso el estado actual no se modifica.
    """
    datos = _leer_json(ruta)
    if datos is _LECTURA_FALLIDA:
        return False
    if not _tiene_forma_valida(datos):
        gestor.ultimo_error = "archivo corrupto"
        return False
    gestor.INVENTARIO.clear()
    for codigo in datos["inventario"]:
        gestor.INVENTARIO[codigo] = datos["inventario"][codigo]
    gestor.VENTAS.clear()
    for venta in datos["ventas"]:
        gestor.VENTAS.append(venta)
    gestor.contador_ventas = datos.get("contador", 0)
    return True


def existe_archivo(ruta: str) -> bool:
    """Indica si ya existe el archivo de datos."""
    return os.path.exists(ruta)
