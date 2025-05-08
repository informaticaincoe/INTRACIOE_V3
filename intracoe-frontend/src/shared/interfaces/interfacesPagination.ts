import { FiltersListadoFacturas } from "./interfaceFacturaJSON";

export interface pagination2 {
  current_page: number;
  page_size: number;
  total_pages: number;
  total_records: number;
}


export interface Pagination { // **correcto
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface Proveedores {
  page?: number;
  limit?: number;
  filters?: FiltersListadoFacturas; //TODO: Mover filtros aqui
}

export interface MovimientoInventarioParams {
  page?: number;
  limit?: number;
  //filters
}

export interface ComprasParams {
  page?: number;
  limit?: number;
  //filters
}

export interface DevolucionComprasParams {
  page?: number;
  limit?: number;
  //filters
}

export interface DevolucionVentasParams {
  page?: number;
  limit?: number;
  //filters
}

export interface ReceptoresParams {
  page?: number;
  limit?: number;
  filter?: any; //TODO: Mover filtros aqui
}

export interface ProveedoressParams {
  page?: number;
  limit?: number;
  // filters?: FiltersListadoFacturas; //TODO: Mover filtros aqui
}

export interface AjusteInventarioParams {
  page?: number;
  limit?: number;
  //filters
}

export interface ProductosParams {
  page?: number;
  limit?: number;
  filter?: string;
  tipo?: string | number;
}