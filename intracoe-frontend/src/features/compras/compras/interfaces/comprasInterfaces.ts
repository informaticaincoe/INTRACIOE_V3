export interface CompraInterface {
    id: number;
    proveedor: number;
    nombreProveedor?: string;
    fecha: any;
    total: number;
    estado: string;
}

export const comprarDefault = {
    id: 1,
    proveedor: 123,
    nombreProveedor: "Proveedor X",
    fecha: new Date(),
    total: 1000,
    estado: 'Pendiente'
};

export interface DetalleCompra {
    codigo: string;
    descripcion: string;
    categoria?: number | null;
    unidad_medida?: number | null;
    precio_unitario: string;
    preunitario: string;
    precio_venta: string;
    cantidad: string;
}

export const DetalleCompraDefault = {
    codigo: "",
    descripcion: "",
    categoria: null,
    unidad_medida: null,
    precio_venta: "",
    cantidad: "",
    precio_unitario: "",
    preunitario: ""
}

export const erroresDetalleCompra = {
    codigo: "",
    descripcion: "",
    categoria: "",
    precio_venta: "",
    cantidad: "",
    precio_unitario: "",
    preunitario: ""
}

export const erroresCompra = {
    proveedor: "",
    estado: ""
}


export interface DetalleCompraPayload {
    codigo: string;
    descripcion: string;
    categoria?: number | null;
    unidad_medida?: number | null;
    precio_unitario: string;
    precio_venta: string;
    preunitario: string;
    cantidad: string;
}

export interface CompraPayload {
    proveedor: number;
    estado: string;
    total: string,
    detalles: DetalleCompraPayload[];
}


export const CompraPayloadDeafult = {
    proveedor: 0,
    fecha: new Date(),
    estado: "Pendiente",
    total: "",
    detalles: [{
        codigo: "",
        descripcion: "",
        categoria: null,
        unidad_medida: null,
        precio_unitario: "",
        preunitario: "",
        precio_venta: "",
        cantidad: "",
    }]
}

export interface detalleCompraInterfaz {
    cantidad: number,
    compra:number,
    id: number,
    precio_unitario:string,
    subtotal:string,
    producto:number,
    nombreProducto?:string
}