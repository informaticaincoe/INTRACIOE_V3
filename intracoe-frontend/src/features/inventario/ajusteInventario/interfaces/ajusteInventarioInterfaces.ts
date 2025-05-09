export interface AjusteInventarioInterfaceResults {
  producto: number;
  nombreProducto?: string;
  almacen: number;
  nombreAlmacen?: string;
  cantidad_ajustada: number;
  motivo: string;
  fecha: Date;
  usuario: string;
}

export interface AjusteInventarioInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: AjusteInventarioInterfaceResults[];
}
