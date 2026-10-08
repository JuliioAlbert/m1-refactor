"""Punto de entrada del gestor de tienda (menu interactivo en consola)."""

import math
from collections.abc import Callable

import gestor
import almacen
import reportes

ARCHIVO_DATOS = "datos_ejemplo.json"


def pedir_numero(mensaje: str) -> float:
    # pide un numero al usuario hasta que escriba algo valido
    while True:
        entrada = input(mensaje)
        try:
            numero = float(entrada)
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
    codigo = input("Codigo: ")
    nombre = input("Nombre: ")
    precio = pedir_numero("Precio: ")
    stock = pedir_entero("Stock inicial: ")
    if not gestor.agregarProducto(codigo, nombre, precio, stock):
        _mostrar_error()
        return
    print("Producto agregado.")


def _opcion_registrar_venta() -> None:
    codigo = input("Codigo del producto: ")
    cantidad = pedir_entero("Cantidad: ")
    cliente = input("Codigo de cliente (enter si no tiene): ")
    venta = gestor.registrar_venta(codigo, cantidad, cliente)
    if venta is None:
        _mostrar_error()
        return
    print(venta["ticket"])


def _opcion_cotizar() -> None:
    codigo = input("Codigo del producto: ")
    cantidad = pedir_entero("Cantidad: ")
    total = gestor.cotizar(codigo, cantidad)
    if total is None:
        _mostrar_error()
        return
    print("Total estimado (con IVA): $" + str(total))


def _opcion_mas_vendidos() -> None:
    for codigo, unidades in reportes.mas_vendidos():
        print(codigo, "->", unidades, "unidades")


def _opcion_stock_bajo() -> None:
    productos_bajos = reportes.productos_stock_bajo()
    if not productos_bajos:
        print("No hay productos con stock bajo.")
        return
    for producto in productos_bajos:
        print(
            "OJO:", producto["nombre"], "solo tiene", producto["stock"], "unidades"
        )


ACCIONES: dict[str, Callable[[], object]] = {
    "1": _opcion_agregar_producto,
    "2": _opcion_registrar_venta,
    "3": _opcion_cotizar,
    "4": reportes.reporte_inventario,
    "5": reportes.resumen_ventas,
    "6": _opcion_mas_vendidos,
    "7": _opcion_stock_bajo,
}


def _cargar_datos_iniciales() -> None:
    if not almacen.existe_archivo(ARCHIVO_DATOS):
        return
    if almacen.cargar_datos(ARCHIVO_DATOS):
        print("Datos cargados de", ARCHIVO_DATOS)
    else:
        _mostrar_error()


def menu() -> None:
    print("Bienvenido al gestor de la tienda La Esquina")
    _cargar_datos_iniciales()
    while True:
        _imprimir_opciones()
        opcion = input("Opcion: ")
        if opcion == "8":
            if almacen.guardar_datos(ARCHIVO_DATOS):
                print("Datos guardados. Hasta luego.")
            else:
                _mostrar_error()
            break
        accion = ACCIONES.get(opcion)
        if accion is None:
            print("Opcion no valida.")
            continue
        accion()


if __name__ == "__main__":
    menu()
