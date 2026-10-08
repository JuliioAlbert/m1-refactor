"""Reportes de la tienda: inventario, ventas y mas vendidos."""

import gestor

STOCK_MINIMO = 5


def formato_dinero(monto: float) -> str:
    """Le da formato de dinero al monto."""
    return "$" + str(round(monto, 2))


def _stock_bajo(producto: gestor.Producto) -> bool:
    return producto["stock"] < STOCK_MINIMO


def productos_stock_bajo() -> list[gestor.Producto]:
    """Regresa la lista de productos con stock por debajo del minimo."""
    productos = gestor.INVENTARIO.values()
    return [producto for producto in productos if _stock_bajo(producto)]


def reporte_inventario() -> str:
    """Arma el reporte del inventario, lo imprime y lo regresa como texto."""
    reporte = "===== INVENTARIO =====\n"
    valor_total = 0
    for producto in gestor.INVENTARIO.values():
        linea = producto["codigo"] + " | " + producto["nombre"] + " | "
        linea = linea + formato_dinero(producto["precio"])
        linea = linea + " | stock: " + str(producto["stock"])
        if _stock_bajo(producto):
            linea = linea + "  <-- STOCK BAJO"
        reporte = reporte + linea + "\n"
        valor_total = valor_total + producto["precio"] * producto["stock"]
    reporte = reporte + "Valor total del inventario: "
    reporte = reporte + formato_dinero(valor_total) + "\n"
    print(reporte)
    return reporte


def total_vendido() -> float:
    """Suma el total (con IVA) de todas las ventas registradas."""
    total = 0
    for venta in gestor.VENTAS:
        total = total + venta["total"]
    return round(total, 2)


def mas_vendidos(n: int = 3) -> list[tuple[str, int]]:
    """Regresa los n productos mas vendidos como lista de (codigo, unidades)."""
    unidades_por_codigo = {}
    for venta in gestor.VENTAS:
        codigo = venta["codigo"]
        unidades_por_codigo[codigo] = (
            unidades_por_codigo.get(codigo, 0) + venta["cantidad"]
        )
    ranking = []
    for codigo in unidades_por_codigo:
        ranking.append((codigo, unidades_por_codigo[codigo]))
    # ordenamiento de burbuja (TODO: algun dia usar sorted)
    for i in range(len(ranking)):
        for j in range(0, len(ranking) - i - 1):
            if ranking[j][1] < ranking[j + 1][1]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
    return ranking[0:n]


def resumen_ventas() -> str:
    """Arma el resumen de ventas del dia, lo imprime y lo regresa."""
    resumen = "===== RESUMEN DE VENTAS =====\n"
    for venta in gestor.VENTAS:
        resumen = resumen + "Folio " + str(venta["folio"]) + ": "
        resumen = resumen + venta["nombre"]
        resumen = resumen + " x" + str(venta["cantidad"]) + " = "
        resumen = resumen + formato_dinero(venta["total"]) + "\n"
    resumen = resumen + "Numero de ventas: " + str(len(gestor.VENTAS)) + "\n"
    resumen = resumen + "Total del dia: " + formato_dinero(total_vendido()) + "\n"
    print(resumen)
    return resumen
