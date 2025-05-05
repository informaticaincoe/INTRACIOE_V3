export interface AjusteInventarioInterface {
    producto: number,
    nombreProducto?: string,
    almacen: number,
    nombreAlmacen?: string,
    cantidad_ajustada: number,
    motivo: string,
    fecha: Date,
    usuario: string
}