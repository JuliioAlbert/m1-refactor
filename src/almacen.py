"""Persistencia del gestor: carga y guardado de datos en JSON."""

import json
import os
from typing import Any

import gestor

_FALLO = object()


def guardar_datos(ruta: str) -> bool:
    """Guarda el inventario, las ventas y el folio actual en un JSON.

    Regresa False si no se puede escribir el archivo.
    """
    d = {}
    d["inventario"] = gestor.INVENTARIO
    d["ventas"] = gestor.VENTAS
    d["contador"] = gestor.contadorVentas
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
    except OSError:
        gestor.ultimo_error = "no se pudo guardar el archivo"
        return False
    return True


def _leer_json(ruta: str) -> Any:
    """Regresa el contenido del JSON o _FALLO (con ultimo_error) si falla."""
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        gestor.ultimo_error = "el archivo no existe"
    except (json.JSONDecodeError, UnicodeDecodeError):
        gestor.ultimo_error = "archivo corrupto"
    except OSError:
        gestor.ultimo_error = "no se pudo leer el archivo"
    return _FALLO


def _tiene_forma_valida(d: Any) -> bool:
    return (
        isinstance(d, dict)
        and isinstance(d.get("inventario"), dict)
        and isinstance(d.get("ventas"), list)
    )


def cargar_datos(ruta: str) -> bool:
    """Lee el archivo JSON y deja los datos en el estado global.

    Regresa False si el archivo no existe, esta corrupto o no se puede leer;
    en ese caso el estado actual no se modifica.
    """
    d = _leer_json(ruta)
    if d is _FALLO:
        return False
    if not _tiene_forma_valida(d):
        gestor.ultimo_error = "archivo corrupto"
        return False
    gestor.INVENTARIO.clear()
    for k in d["inventario"]:
        gestor.INVENTARIO[k] = d["inventario"][k]
    gestor.VENTAS.clear()
    for v in d["ventas"]:
        gestor.VENTAS.append(v)
    gestor.contadorVentas = d.get("contador", 0)
    return True


def hayArchivo(ruta: str) -> bool:
    # checa si ya existe el archivo de datos
    return os.path.exists(ruta)
