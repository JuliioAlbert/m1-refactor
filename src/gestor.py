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
contador_ventas: int = 0
ultimo_error: str = ""

# Reglas de negocio: descuentos (minimo de subtotal, tasa), de mayor a menor
DESCUENTOS_VOLUMEN = ((1000, 0.10), (500, 0.05))
PREFIJO_VIP = "VIP"
MONTO_MINIMO_VIP = 200
DESCUENTO_VIP = 0.02
TASA_IVA = 0.16

# Motivos de error que se dejan en ultimo_error
ERROR_CODIGO_VACIO = "codigo vacio"
ERROR_NO_EXISTE = "producto no existe"
ERROR_YA_EXISTE = "el producto ya existe"
ERROR_PRECIO = "precio invalido"
ERROR_STOCK = "stock invalido"
ERROR_STOCK_NEGATIVO = "el stock no puede quedar negativo"
ERROR_CANTIDAD = "cantidad invalida"
ERROR_STOCK_INSUFICIENTE = "stock insuficiente"


def reiniciar_sistema() -> None:
    """Borra todo el estado del sistema (inventario, ventas y folios)."""
    global contador_ventas, ultimo_error
    INVENTARIO.clear()
    VENTAS.clear()
    contador_ventas = 0
    ultimo_error = ""


def agregarProducto(codigo: str | None, nombre: str, precio: float, stock: int) -> bool:
    # valida los datos y da de alta un producto en el inventario
    global ultimo_error
    if not codigo:
        ultimo_error = ERROR_CODIGO_VACIO
        return False
    if codigo in INVENTARIO:
        ultimo_error = ERROR_YA_EXISTE
        return False
    if precio <= 0:
        ultimo_error = ERROR_PRECIO
        return False
    if stock < 0:
        ultimo_error = ERROR_STOCK
        return False
    producto: Producto = {
        "codigo": codigo,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
    }
    INVENTARIO[codigo] = producto
    return True


def eliminar_producto(codigo: str) -> bool:
    """Quita un producto del inventario. Regresa False si no existe."""
    global ultimo_error
    if codigo in INVENTARIO:
        del INVENTARIO[codigo]
        return True
    ultimo_error = ERROR_NO_EXISTE
    return False


def actualizar_stock(codigo: str, cantidad: int) -> bool:
    """Suma unidades al stock (o resta si la cantidad es negativa)."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = ERROR_NO_EXISTE
        return False
    nuevo_stock = INVENTARIO[codigo]["stock"] + cantidad
    if nuevo_stock < 0:
        ultimo_error = ERROR_STOCK_NEGATIVO
        return False
    INVENTARIO[codigo]["stock"] = nuevo_stock
    return True


def buscarProducto(texto: str) -> list[Producto]:
    # busca productos cuyo nombre contenga el texto (sin importar mayusculas)
    encontrados = []
    for producto in INVENTARIO.values():
        if texto.lower() in producto["nombre"].lower():
            encontrados.append(producto)
    return encontrados


def _cantidad_invalida(cantidad: int | None) -> bool:
    return cantidad is None or cantidad <= 0


def _validar_venta(codigo: str | None, cantidad: int | None) -> Producto | None:
    """Regresa el producto si la venta es valida; si no, fija ultimo_error."""
    global ultimo_error
    if not codigo:
        ultimo_error = ERROR_CODIGO_VACIO
        return None
    if codigo not in INVENTARIO:
        ultimo_error = ERROR_NO_EXISTE
        return None
    if _cantidad_invalida(cantidad):
        ultimo_error = ERROR_CANTIDAD
        return None
    if INVENTARIO[codigo]["stock"] < cantidad:
        ultimo_error = ERROR_STOCK_INSUFICIENTE
        return None
    return INVENTARIO[codigo]


def _descuento_volumen(subtotal: float) -> float:
    """Descuento por volumen: 10% desde $1000, 5% desde $500."""
    for minimo, tasa in DESCUENTOS_VOLUMEN:
        if subtotal >= minimo:
            return subtotal * tasa
    return 0


def _es_vip(cliente: str | None) -> bool:
    """Los clientes cuyo codigo empieza con VIP tienen descuento extra."""
    return bool(cliente) and cliente.startswith(PREFIJO_VIP)


def _descuento_vip(
    subtotal: float, descuento_previo: float, cliente: str | None
) -> float:
    """Extra VIP: solo si la compra (ya con descuento) pasa del monto minimo."""
    if _es_vip(cliente) and subtotal - descuento_previo > MONTO_MINIMO_VIP:
        return subtotal * DESCUENTO_VIP
    return 0


def _armar_ticket(venta: Venta) -> str:
    """Arma el ticket en texto plano a partir de la venta."""
    ticket = "TIENDA LA ESQUINA\n"
    ticket = ticket + "----------------------------\n"
    ticket = ticket + "Folio: " + str(venta["folio"]) + "\n"
    ticket = ticket + venta["nombre"] + " x" + str(venta["cantidad"]) + "\n"
    ticket = ticket + "Subtotal: $" + str(venta["subtotal"]) + "\n"
    if venta["descuento"] > 0:
        ticket = ticket + "Descuento: -$" + str(venta["descuento"]) + "\n"
    ticket = ticket + "IVA: $" + str(venta["impuesto"]) + "\n"
    ticket = ticket + "TOTAL: $" + str(venta["total"]) + "\n"
    return ticket


def registrar_venta(
    codigo: str | None, cantidad: int | None, cliente: str | None = ""
) -> Venta | None:
    """Registra una venta completa.

    Valida los datos, calcula descuentos e impuestos, descuenta el stock,
    genera el folio, arma el ticket y guarda el registro en la lista de
    ventas. Si algo falla regresa None y deja el motivo en ultimo_error.
    """
    global contador_ventas
    producto = _validar_venta(codigo, cantidad)
    if producto is None:
        return None
    subtotal = producto["precio"] * cantidad
    descuento = _descuento_volumen(subtotal)
    descuento = descuento + _descuento_vip(subtotal, descuento, cliente)
    base_gravable = subtotal - descuento
    impuesto = base_gravable * TASA_IVA
    producto["stock"] = producto["stock"] - cantidad
    contador_ventas = contador_ventas + 1
    venta = {}
    venta["folio"] = contador_ventas
    venta["codigo"] = codigo
    venta["nombre"] = producto["nombre"]
    venta["cantidad"] = cantidad
    venta["subtotal"] = round(subtotal, 2)
    venta["descuento"] = round(descuento, 2)
    venta["impuesto"] = round(impuesto, 2)
    venta["total"] = round(base_gravable + impuesto, 2)
    venta["cliente"] = cliente
    venta["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    venta["ticket"] = _armar_ticket(venta)
    VENTAS.append(venta)
    return venta


def cotizar(codigo: str, cantidad: int | None) -> float | None:
    """Calcula cuanto costaria una compra sin registrar la venta."""
    global ultimo_error
    if codigo not in INVENTARIO:
        ultimo_error = ERROR_NO_EXISTE
        return None
    if _cantidad_invalida(cantidad):
        ultimo_error = ERROR_CANTIDAD
        return None
    subtotal = INVENTARIO[codigo]["precio"] * cantidad
    base_gravable = subtotal - _descuento_volumen(subtotal)
    return round(base_gravable + base_gravable * TASA_IVA, 2)
