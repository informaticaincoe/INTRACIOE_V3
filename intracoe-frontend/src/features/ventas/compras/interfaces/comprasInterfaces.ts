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
    codigo: string;
    descripcion: string;
    categoria?: number | null;
    unidad_medida?: number | null;
    precio_unitario: string;
    preunitario: string;
    precio_venta: string;
    cantidad: number;
}

export const DetalleCompraDefault = {
    codigo: "",
    descripcion: "",
    categoria: null,
    unidad_medida: null,
    precio_venta: "",
    cantidad: 0,
    precio_unitario: "",
    preunitario: ""
}


export interface DetalleCompraPayload {
    codigo: string;
    descripcion: string;
    categoria?: number | null;
    unidad_medida?: number | null;
    precio_unitario: string;
    precio_venta: string;
    preunitario: string;
    cantidad: number;
}

export interface CompraPayload {
    proveedor: number;
    estado: string;
    detalles: DetalleCompraPayload[];
}


export const CompraPayloadDeafult = {
    proveedor: 0,
    estado: "",
    detalles: [{
        codigo: "",
        descripcion: "",
        categoria: null,
        unidad_medida: null,
        precio_unitario: "",
        preunitario: "",
        precio_venta: "",
        cantidad: 0,
    }]
}
