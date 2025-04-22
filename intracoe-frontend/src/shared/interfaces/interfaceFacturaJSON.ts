export interface FacturaJSON {
  emisorJSON: EmisorJSON;
}

export interface EmisorJSON {
  nit: string;
  nrc: string;
  nombre: string;
  codActividad: string;
  descActividad: string;
  nombreComercial: string;
  tipo_establecimiento_codigo: string;
  departamento: string;
  municipio: string;
  complemento: string;
  telefono: string;
  correo: string;
  codEstableMH: string;
  codEstable: string;
  codPuntoVentaMH: string;
  codPuntoVenta: string;
}

export interface FacturaListado {
  count: number;
  next: string;
  previous: string | null;
  results: ListResult;
}

export interface ListResult {
  codigo_generacion: string;
  fecha_emision: string;
  firmado: boolean;
  hora_emision: string;
  id: number;
  numero_control: string;
  recibido_mh: boolean;
  tipo_dte: number;
}

export interface ListFactura {
  current_page:number;
  page_size: number;
  total_pages: number;
  total_records: number;
  results:  ListResult[]
}

export interface Filters {
  recibido_mh: boolean | null;
  sello_recepcion: string | null;
  has_sello_recepcion: boolean | null;
  tipo_dte: any | null;
  estado: any | null;
  estado_invalidacion: any | null;
}
