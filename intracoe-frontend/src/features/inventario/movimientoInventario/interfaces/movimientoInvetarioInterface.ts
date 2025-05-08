import { Pagination } from "../../../../shared/interfaces/interfacesPagination"

export interface movimientoInterface {
    count: number;
    page_size: number;
    current_page: number;
    has_next: boolean;
    has_previous: boolean;
    results: resultsMovimiento[]    
}


export interface resultsMovimiento{
    almacen:number,
    cantidad:number,
    fecha:Date,
    id:number,
    producto:number,
    nombreProducto?:string,
    nombreAlmacen?:string,
    referencia:string,
    tipo: string
}