"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

STOCK_MINIMO = 5


def hacer_cosa(v: float) -> str:
    # le da formato de dinero al numero
    return "$" + str(round(v, 2))


def _stock_bajo(p: gestor.Producto) -> bool:
    return p["stock"] < STOCK_MINIMO


def productos_stock_bajo() -> list[gestor.Producto]:
    """Regresa la lista de productos con stock por debajo del minimo."""
    return [p for p in gestor.INVENTARIO.values() if _stock_bajo(p)]


def reporte_inventario() -> str:
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    s = "===== INVENTARIO =====\n"
    aux = 0
    for k in gestor.INVENTARIO:
        p = gestor.INVENTARIO[k]
        linea = p["codigo"] + " | " + p["nombre"] + " | "
        linea = linea + hacer_cosa(p["precio"]) + " | stock: " + str(p["stock"])
        if _stock_bajo(p):
            linea = linea + "  <-- STOCK BAJO"
        s = s + linea + "\n"
        aux = aux + p["precio"] * p["stock"]
    s = s + "Valor total del inventario: " + hacer_cosa(aux) + "\n"
    print(s)
    return s


def total_vendido() -> float:
    """Suma el total (con IVA) de todas las ventas registradas."""
    t = 0
    for v in gestor.VENTAS:
        t = t + v["total"]
    return round(t, 2)


def mas_vendidos(n: int = 3) -> list[tuple[str, int]]:
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    aux = {}
    for v in gestor.VENTAS:
        aux[v["codigo"]] = aux.get(v["codigo"], 0) + v["cantidad"]
    temp = []
    for k in aux:
        temp.append((k, aux[k]))
    # ordenamiento de burbuja (TODO: algun dia usar sorted)
    for i in range(len(temp)):
        for j in range(0, len(temp) - i - 1):
            if temp[j][1] < temp[j + 1][1]:
                t = temp[j]
                temp[j] = temp[j + 1]
                temp[j + 1] = t
    return temp[0:n]


def resumen_ventas() -> str:
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    s = "===== RESUMEN DE VENTAS =====\n"
    for v in gestor.VENTAS:
        s = s + "Folio " + str(v["folio"]) + ": " + v["nombre"]
        s = s + " x" + str(v["cantidad"]) + " = " + hacer_cosa(v["total"]) + "\n"
    s = s + "Numero de ventas: " + str(len(gestor.VENTAS)) + "\n"
    s = s + "Total del dia: " + hacer_cosa(total_vendido()) + "\n"
    print(s)
    return s
