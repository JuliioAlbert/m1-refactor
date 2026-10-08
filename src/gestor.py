"""Modulo principal del gestor de inventario y ventas de "La Esquina"."""

from datetime import datetime
from typing import TypedDict


class Producto(TypedDict):
    codigo: str
    nombre: str
    precio: float
    stock: int


class Venta(TypedDict):
    folio: int
    codigo: str
    nombre: str
    cantidad: int
    subtotal: float
    descuento: float
    impuesto: float
    total: float
    cliente: str | None
    fecha: str
    ticket: str

# ---------------------------------------------------------------
# Estado global de la aplicacion (inventario, ventas y contadores)
# ---------------------------------------------------------------
INVENTARIO: dict[str, Producto] = {}
VENTAS: list[Venta] = []
contadorVentas: int = 0
ultimo_error: str = ""


def reiniciar_sistema() -> None:
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contadorVentas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contadorVentas = 0
    ultimo_error = ""


def agregarProducto(
    codigo: str | None, nombre: str, precio: float, stock: int
) -> bool:
    # valida los datos y da de alta un producto en el inventario
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return False
    if codigo in INVENTARIO:
        ultimo_error = "el producto ya existe"
        return False
    if precio <= 0:
        ultimo_error = "precio invalido"
        return False
    if stock < 0:
        ultimo_error = "stock invalido"
        return False
    x: Producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
    }
    INVENTARIO[codigo] = x
    return True


def eliminar_producto(codigo: str) -> bool:
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = "producto no existe"
    return False


def actualizar_stock(codigo: str, cantidad: int) -> bool:
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return False
    aux = INVENTARIO[codigo]["stock"] + cantidad
    if aux < 0:
        ultimo_error = "el stock no puede quedar negativo"
        return False
    INVENTARIO[codigo]["stock"] = aux
    return True


def buscarProducto(texto: str) -> list[Producto]:
    # busca productos cuyo nombre contenga el texto (sin importar mayusculas)
    temp2 = []
    for k in INVENTARIO:
        if texto.lower() in INVENTARIO[k]["nombre"].lower():
            temp2.append(INVENTARIO[k])
    return temp2


def _validar_venta(codigo: str | None, cantidad: int | None) -> Producto | None:
    """Regresa el producto si la venta es valida; si no, fija ultimo_error."""
    global ultimo_error
    if codigo is None or codigo == "":
        ultimo_error = "codigo vacio"
        return None
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return None
    if INVENTARIO[codigo]["stock"] < cantidad:
        ultimo_error = "stock insuficiente"
        return None
    return INVENTARIO[codigo]


def _descuento_volumen(subtotal: float) -> float:
    """Descuento por volumen: 10% desde $1000, 5% desde $500."""
    if subtotal >= 1000:
        return subtotal * 0.10
    if subtotal >= 500:
        return subtotal * 0.05
    return 0


def _es_vip(cliente: str | None) -> bool:
    """Los clientes cuyo codigo empieza con VIP tienen descuento extra."""
    return bool(cliente) and cliente[:3] == "VIP"


def _armar_ticket(venta: Venta) -> str:
    """Arma el ticket en texto plano a partir de la venta."""
    t = "TIENDA LA ESQUINA\n"
    t = t + "----------------------------\n"
    t = t + "Folio: " + str(venta["folio"]) + "\n"
    t = t + venta["nombre"] + " x" + str(venta["cantidad"]) + "\n"
    t = t + "Subtotal: $" + str(venta["subtotal"]) + "\n"
    if venta["descuento"] > 0:
        t = t + "Descuento: -$" + str(venta["descuento"]) + "\n"
    t = t + "IVA: $" + str(venta["impuesto"]) + "\n"
    t = t + "TOTAL: $" + str(venta["total"]) + "\n"
    return t


def registrar_venta(
    codigo: str | None, cantidad: int | None, cliente: str | None = ""
) -> Venta | None:
    """Registra una venta completa.

    Valida los datos, calcula descuentos e impuestos, descuenta el stock,
    genera el folio, arma el ticket y guarda el registro en la lista de
    ventas. Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contadorVentas
    producto = _validar_venta(codigo, cantidad)
    if producto is None:
        return None
    subtotal = producto["precio"] * cantidad
    desc = _descuento_volumen(subtotal)
    # el extra VIP aplica solo si la compra (ya con descuento) pasa de cierto monto
    if _es_vip(cliente) and subtotal - desc > 200:
        desc = desc + subtotal * 0.02
    base = subtotal - desc
    impuesto = base * 0.16
    producto["stock"] = producto["stock"] - cantidad
    contadorVentas = contadorVentas + 1
    venta = {}
    venta["folio"] = contadorVentas
    venta["codigo"] = codigo
    venta["nombre"] = producto["nombre"]
    venta["cantidad"] = cantidad
    venta["subtotal"] = round(subtotal, 2)
    venta["descuento"] = round(desc, 2)
    venta["impuesto"] = round(impuesto, 2)
    venta["total"] = round(base + impuesto, 2)
    venta["cliente"] = cliente
    venta["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    venta["ticket"] = _armar_ticket(venta)
    VENTAS.append(venta)
    return venta


def cotizar(codigo: str, cantidad: int | None) -> float | None:
    """Calcula cuanto costaria una compra sin registrar la venta."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = "producto no existe"
        return None
    if cantidad is None or cantidad <= 0:
        ultimo_error = "cantidad invalida"
        return None
    subtotal = INVENTARIO[codigo]["precio"] * cantidad
    base = subtotal - _descuento_volumen(subtotal)
    return round(base + base * 0.16, 2)
