import { Nullable } from 'primereact/ts-helpers';

export interface ActivitiesData {
  id: number;
  codigo: string;
  descripcion: string;
}

export interface contingenciaData {
  id: number;
  codigo: string;
  descripcion: string;
  motivo_contingencia: string;
}

export interface tipoDocTributarioData {
  id: number;
  codigo: string;
  descripcion: string;
  version: string;
}

export interface ActivitiesDataNew {
  codigo: string;
  descripcion: string;
}

export const defaultEmisorData: EmisorInterface = {
  nit: '',
  nrc: '',
  nombre_razon_social: '',
  nombre_comercial: '',
  direccion_comercial: '',
  telefono: '',
  email: '',
  codigo_punto_venta: '', //codigo
  codigo_establecimiento: '',
  nombre_establecimiento: null,
  tipoestablecimiento: {
    id: '',
    descripcion: '',
    code: '',
  },
  departamento: {
    id: '',
    descripcion: '',
    code: '',
  },
  municipio: {
    id: '',
    descripcion: '',
    code: '',
  },
  ambiente: {
    id: '',
    descripcion: '',
    code: '',
  },
  tipo_documento: {
    id: '',
    descripcion: '',
    code: '',
  },
  actividades_economicas: [],
};

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

export const ReceptorDefault: ReceptorInterface = {
  id: '',
  tipo_documento: {
    id: '',
    descripcion: '',
    code: '',
  },
  num_documento: '',
  nrc: '',
  nombre: '',
  actividades_economicas: [],
  municipio: { id: '', descripcion: '', code: '' },
  direccion: '',
  telefono: '',
  correo: '',
  nombre_comercial: '',
};

export const ReceptorRequestDefault: ReceptorRequestInterface = {
  id: '',
  tipo_documento: {
    id: '',
    descripcion: '',
    code: '',
  },
  num_documento: '',
  nrc: '',
  nombre: '',
  actividades_economicas: [],
  municipio: '',
  direccion: '',
  telefono: '',
  correo: '',
  nombre_comercial: '',
  tipo_receptor: '',
};

export interface ReceptorInterface {
  id: string;
  tipo_documento: TipoDocumento;
  num_documento: string;
  nrc: string;
  nombre: string;
  actividades_economicas: ActivitiesData[];
  municipio: { id: string; descripcion: string; code: string };
  direccion: string;
  telefono: string;
  correo: string;
  nombre_comercial: string;
}

export interface ReceptorRequestInterface {
  id: string;
  tipo_documento: TipoDocumento;
  num_documento: string;
  tipo_receptor: string;
  nrc: string;
  nombre: string;
  actividades_economicas: ActivitiesData[];
  municipio: string;
  direccion: string;
  telefono: string;
  correo: string;
  nombre_comercial: string;
}

export interface TipoDocumento {
  id: string;
  descripcion: string;
  code: string;
}

export interface TipoDocumentoDropDown {
  name: string;
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

export interface DepartamentoCatalogo {
  id: string;
  descripcion: string;
  codigo: string;
  pais: number;
}

export interface PaisCatalogo {
  id: string;
  descripcion: string;
  codigo: string;
}

export interface Municipio {
  id: string;
  descripcion: string;
  code: string;
}

export const RequestEmpresaDefault = {
  nit: '',
  nrc: '',
  nombre_razon_social: '',
  nombre_comercial: '',
  direccion_comercial: '',
  telefono: '',
  email: '',
  codigo_establecimiento: '',
  codigo_punto_venta: '',
  nombre_establecimiento: '',
  tipoestablecimiento: '',
  departamento: '',
  municipio: '',
  ambiente: '',
  tipo_documento: '',
  actividades_economicas: [],
  clave_privada: '',
  clave_publica: '',
};

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
  nombre_establecimiento: string;
  tipoestablecimiento: string;
  departamento: string;
  municipio: string;
  ambiente: string;
  tipo_documento: string;
  actividades_economicas: string[]; // Array de IDs de actividades económicas
  clave_privada: string;
  clave_publica: string;
}

export interface Product {
  id: number;
  codigo: string;
  descripcion: string;
  precio_unitario: string;
  cantidad: number;
  no_grabado: boolean;
  descuento: number;
  iva_unitario: number;
  total_neto: number;
  total_iva: number;
  total_con_iva: number;
  iva_percibido: number;
  seleccionar: boolean;
}

export interface Categoria {
  id: number;
  // Otros campos relevantes
  nombre: string;
}

export interface TipoUnidadMedida {
  id: number;
  codigo: string;
  descripcion: string;
}

export interface Impuesto {
  id: number;
  // Otros campos relevantes
  nombre: string;
  porcentaje: number;
}

export interface TipoItem {
  id: number;
  // Otros campos relevantes
  nombre: string;
}

export interface Tributo {
  id: number;
  // Otros campos relevantes
  nombre: string;
}

export interface Almacen {
  id: number;
  // Otros campos relevantes
  nombre: string;
  ubicacion: string;
  resposable: string;
}

export interface ProductoRequest {
  codigo: string;
  descripcion: string;
  categoria?: Categoria | null;
  unidad_medida?: number | null;
  preunitario: number;
  precio_compra: number;
  precio_venta: number;
  stock: number;
  stock_minimo: number;
  stock_maximo: number;
  impuestos: number[] | null;
  tipo_item?: number | null;
  referencia_interna?: string | null;
  tributo: number;
  precio_iva: boolean;
  maneja_lotes: boolean;
  fecha_vencimiento?: Nullable<Date> | string;
  almacenes: number[];
  imagen?: File | null;
}

export const productoInicial: ProductoRequest = {
  codigo: '',
  descripcion: '',
  // categoria: null,
  unidad_medida: null,
  preunitario: 0,
  precio_compra: 0,
  precio_venta: 0,
  stock: 0,
  stock_minimo: 0,
  stock_maximo: 0,
  impuestos: [],
  tipo_item: null,
  referencia_interna: null,
  tributo: 0,
  precio_iva: false,
  maneja_lotes: false,
  fecha_vencimiento: null,
  almacenes: [],
  imagen: null,
};

export interface TipoGeneracionDocumentoInterface {
  id: number;
  codigo: string;
  descripcion: string;
}

export interface TipoDTE {
  id: string;
  codigo: string;
  descripcion: string;
  version: number | null;
}

export interface TipoTributos {
  id: number;
  codigo: string;
  descripcion: string;
}

export interface Tributos {
  id: number;
  codigo: string;
  descripcion: string;
  valor_tributo: string;
  tipo_tributo: number;
  tipo_valor: number;
}

export interface ConfiguracionFacturaInterface {
  id: number;
  codigo: string;
  descripcion: string;
}

export interface ProductoResponse {
  id: number;
  codigo: string;
  descripcion: string;
  categoria: Categoria | null;
  unidad_medida: TipoUnidadMedida | null;
  preunitario: number;
  precio_compra: number;
  precio_venta: number;
  stock: number;
  stock_minimo: number;
  stock_maximo: number;
  impuestos: Impuesto[];
  tipo_item: TipoItem | null;
  referencia_interna: string | null;
  tributo: number; //TODO: Verificar que sea un arreglo de tributos
  maneja_lotes: boolean;
  fecha_vencimiento: string | null;
  almacenes: Almacen[];
  imagen: string | null;
  creado: string;
  actualizado: string;
}

// Interfaces para las relaciones de claves foráneas (si es necesario)
export interface Categoria {
  id: number;
  nombre: string;
}

export interface TipoUnidadMedida {
  id: number;
  nombre: string;
}

export interface Impuesto {
  id: number;
  nombre: string;
  porcentaje: number;
}

export interface TipoItem {
  id: number;
  nombre: string;
}

export interface Tributo {
  id: number;
  nombre: string;
}

export interface Almacen {
  id: number;
  nombre: string;
}

export interface Descuento {
  id: number;
  porcentaje: number;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  estdo: boolean;
}

export const DescuentoDefault = {
  id: 0,
  porcentaje: 0,
  descripcion: '',
  fecha_inicio: '',
  fecha_fin: '',
  estdo: false,
};

export interface FacturaDetalleItem {
  monto_a_aumentar: number;
  cantidad_editada: number;
  cantidad: number;
  codigo: string;
  descripcion: string;
  descuento: string;
  iva_unitario: string;
  neto_unitario: string;
  precio_unitario: string;
  producto_id: number;
  total_incl: string;
  total_iva: string;
  total_neto: string;
}

export interface FacturaReceptor {
  id: number;
  nombre: string;
  num_documento: string;
  direccion: string;
  telefono: string;
  correo: string;
}

export interface FacturaPorCodigoGeneracionResponse {
  codigo_generacion: string;
  tipo_documento: string;
  num_documento: string;
  fecha_emision: string; // ISO format: "YYYY-MM-DD"
  fecha_vencimiento: string; // Puede ser igual a fecha_emision
  total: string;
  receptor: FacturaReceptor;
  productos: FacturaDetalleItem[];
}

export interface TipoGeneracionFactura {
  name: string;
  code: string;
}

export interface Descuentos {
  descuentoGeneral: number;
  descuentoGravado: number;
}

export interface pagination {
  current_page: number;
  page_size: number;
  total_pages: number;
  total_records: number;
}

export interface TableListadoFacturasContainerProps {
  data: any;
  pagination: pagination;
  onPageChange: (event: any) => void;
}


export interface Perfil {
  usuario: string;
  correo: string;
}

export interface password {
  newPassword: string;
  password: string;
  confirmPassword: string;
}