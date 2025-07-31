export interface ProveedorInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: ProveedorResultInterface[];
}

export interface ProveedorResultInterface {
  id: number;
  nombre: string;
  ruc_nit: string;
  contacto?: string | null;
  telefono?: string | null;
  email?: string | null;
  direccion?: string | null;
  condiciones_pago?: string | null;
}
