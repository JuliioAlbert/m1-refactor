"""Punto de entrada del gestor de tienda (menu interactivo en consola)."""

import math
from collections.abc import Callable

import gestor
import almacen
import reportes

ARCHIVO = "datos_ejemplo.json"


def pedir_numero(mensaje: str) -> float:
    # pide un numero al usuario hasta que escriba algo valido
    while True:
        temp2 = input(mensaje)
        try:
            numero = float(temp2)
        except ValueError:
            numero = math.nan
        if math.isfinite(numero):
            return numero
        print("Eso no es un numero, intenta de nuevo.")


def pedir_entero(mensaje: str) -> int:
    # pide un numero entero (acepta 2 o 2.0, rechaza fracciones)
    while True:
        numero = pedir_numero(mensaje)
        if numero.is_integer():
            return int(numero)
        print("Debe ser un numero entero, intenta de nuevo.")


def _mostrar_error() -> None:
    print("Error:", gestor.ultimo_error)


def _imprimir_opciones() -> None:
    print("")
    print("1) Agregar producto")
    print("2) Registrar venta")
    print("3) Cotizar")
    print("4) Reporte de inventario")
    print("5) Resumen de ventas")
    print("6) Mas vendidos")
    print("7) Alertas de stock bajo")
    print("8) Guardar y salir")


def _opcion_agregar_producto() -> None:
    c = input("Codigo: ")
    n = input("Nombre: ")
    p = pedir_numero("Precio: ")
    s = pedir_entero("Stock inicial: ")
    if gestor.agregarProducto(c, n, p, s):
        print("Producto agregado.")
    else:
        _mostrar_error()


def _opcion_registrar_venta() -> None:
    c = input("Codigo del producto: ")
    cant = pedir_entero("Cantidad: ")
    cli = input("Codigo de cliente (enter si no tiene): ")
    v = gestor.registrar_venta(c, cant, cli)
    if v is not None:
        print(v["ticket"])
    else:
        _mostrar_error()


def _opcion_cotizar() -> None:
    c = input("Codigo del producto: ")
    cant = pedir_entero("Cantidad: ")
    t = gestor.cotizar(c, cant)
    if t is not None:
        print("Total estimado (con IVA): $" + str(t))
    else:
        _mostrar_error()


def _opcion_mas_vendidos() -> None:
    for par in reportes.mas_vendidos():
        print(par[0], "->", par[1], "unidades")


def _opcion_stock_bajo() -> None:
    bajos = reportes.productos_stock_bajo()
    if len(bajos) == 0:
        print("No hay productos con stock bajo.")
    else:
        for p in bajos:
            print("OJO:", p["nombre"], "solo tiene", p["stock"], "unidades")


ACCIONES: dict[str, Callable[[], object]] = {
    "1": _opcion_agregar_producto,
    "2": _opcion_registrar_venta,
    "3": _opcion_cotizar,
    "4": reportes.reporte_inventario,
    "5": reportes.resumen_ventas,
    "6": _opcion_mas_vendidos,
    "7": _opcion_stock_bajo,
}


def menu() -> None:
    print("Bienvenido al gestor de la tienda La Esquina")
    if almacen.hayArchivo(ARCHIVO):
        if almacen.cargar_datos(ARCHIVO):
            print("Datos cargados de", ARCHIVO)
        else:
            _mostrar_error()
    while True:
        _imprimir_opciones()
        op = input("Opcion: ")
        if op == "8":
            if almacen.guardar_datos(ARCHIVO):
                print("Datos guardados. Hasta luego.")
            else:
                _mostrar_error()
            break
        accion = ACCIONES.get(op)
        if accion is None:
            print("Opcion no valida.")
        else:
            accion()


if __name__ == "__main__":
    menu()
