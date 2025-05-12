import {
  ActivitiesData,
  Ambiente,
  Departamento,
  Municipio,
  ReceptorRequestDefault,
  TipoDocumento,
  TipoEstablecimiento,
} from '../../../../shared/interfaces/interfaces';

export interface ReceptorInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: ReceptorResult[];
}

export interface ReceptorResult {
  nit: string;
  nrc: string;
  nombre_razon_social: string;
  nombre_comercial: string;
  direccion_comercial: string;
  telefono: string;
  email: string;
  codigo_establecimiento: string;
  codigo_punto_venta: string;
  nombre_establecimiento: string | null;
  tipoestablecimiento: TipoEstablecimiento;
  departamento: Departamento;
  municipio: Municipio;
  ambiente: Ambiente;
  tipo_documento: TipoDocumento;
  actividades_economicas: ActivitiesData[];
}

ReceptorRequestDefault;
