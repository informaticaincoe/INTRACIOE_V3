export interface DevolucionCompra {
    count: number;
    page_size: number;
    current_page: number;
    has_next: boolean;
    has_previous: boolean;
    results: DevolucionCompraResult[]
}

export interface DevolucionCompraResult {
    id: number;
    compra: number;
    usuario: string;
    motivo: string;
    estado: string;
    detalles_creados: DetalleCreado[];
}

export interface DetalleCreado {
    cantidad: number;
    motivo_detalle: string;
    producto: number;
}