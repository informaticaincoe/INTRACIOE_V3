export interface DevolucionVentaInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: DevolucionVentaDetalleInterfaceResult[];
}

export interface DevolucionVentaDetalleInterfaceResult {
  id: number;
  proveedor: number;
  nombreProveedor?: string;
  fecha: any;
  total: number;
  estado: string;
}
