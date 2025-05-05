export interface CompraInterface {
    id: number;
    proveedor: number;
    fecha: string;
    total: number;
    estado: 'Pendiente' | 'Pagado' | 'Cancelado';
}