import { Almacen, ProductoResponse } from '../../../../shared/interfaces/interfaces';

export interface AjusteInventarioInterface {
    producto: ProductoResponse,
    almacen: Almacen,
    cantidad_ajustada: number,
    motivo: string,
    fecha: Date,
    usuario: string
} 