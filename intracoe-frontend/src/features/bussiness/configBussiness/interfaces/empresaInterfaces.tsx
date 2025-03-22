import { ActivitiesData } from '../../../facturacion/activities/interfaces/activitiesData';

export interface EmisorInterface {
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
  actividades_economicas: ActivitiesData[]; // Array de IDs de actividades económicas
}

export interface TipoDocumento {
  id: string;
  descripcion: string;
  code: string;
}

export interface Ambiente {
  id: string;
  descripcion: string;
  code: string;
}
export interface TipoEstablecimiento {
  id: string;
  descripcion: string;
  code: string;
}
export interface Departamento {
  id: string;
  descripcion: string;
  code: string;
}

export interface Municipio {
  id: string;
  descripcion: string;
  code: string;
}

export interface RequestEmpresa {
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
  tipoestablecimiento: string;
  departamento: string;
  municipio: string;
  ambiente: string;
  tipo_documento: string;
  actividades_economicas: string[]; // Array de IDs de actividades económicas
}
