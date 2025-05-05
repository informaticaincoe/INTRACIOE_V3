export interface CompraInterface {
    id: number;
    proveedor: number;
    nombreProveedor?: string;
    fecha: Date;
    total: number;
    estado: string;
}

export const comprarDefault = {
    id: 1,
    proveedor: 123,
    nombreProveedor: "Proveedor X",
    fecha: new Date(),
    total: 1000,
    estado: 'Pagado'
};

export interface DetalleCompra {
    compra: number,
    producto: number,
    cantidad: number
    precio_unitario: number,
    subtotal: number,
}

export const DetalleCompraDefailt = {
    compra: 0,
    producto: 0,
    cantidad: 0,
    precio_unitario: 0,
    subtotal: 0,
}