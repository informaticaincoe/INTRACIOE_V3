import { Emisor, Identificacion } from "./facturaPdfInterfaces";

export interface FacturaResponseSujetoExcluido {
  id: number;
  detalles: number[];
  version: number;
  numero_control: string;
  codigo_generacion: string;
  motivocontin: string | null;
  fecha_emision: string;
  hora_emision: string;
  total_no_sujetas: string;
  total_exentas: string;
  total_gravadas: string;
  sub_total_ventas: string;
  descuen_no_sujeto: string;
  descuento_exento: string;
  descuento_gravado: string;
  por_descuento: string;
  total_descuento: string;
  sub_total: string;
  iva_retenido: string;
  retencion_renta: string;
  total_operaciones: string;
  total_no_gravado: string;
  total_pagar: string;
  total_letras: string;
  total_iva: string;
  iva_percibido: string;
  saldo_favor: string | null;
  formas_Pago: any;
  firmado: boolean;
  json_original: JsonDteSujetoExcluido;
  json_firmado: any; 
  sello_recepcion: any;
  recibido_mh: boolean;
  estado: boolean;
  base_imponible: boolean;
  tipo_dte: number;
  tipoModelo: number;
  contingencia: boolean;
  tipocontingencia: any; 
  tipomoneda: number;
  dteemisor: number;
  dtereceptor: number;
  condicion_operacion: number;
}

export interface JsonDteSujetoExcluido {
  identificacion: Identificacion;
  emisor: Emisor;
  sujetoExcluido: SujetoExcluido;
  cuerpoDocumento: CuerpoDocumentoSujetoExcluido[];
  resumen: ResumenSujetoExcluido;
  apendice: any; // null en este caso, pero podrías tiparlo mejor si es necesario
  jsonRespuestaMh: JsonRespuestaMh;
}

export interface SujetoExcluido {
  tipoDocumento: string;
  numDocumento: string;
  nombre: string;
  codActividad: string;
  descActividad: string;
  direccion: Direccion;
  telefono: string;
  correo: string;
}

export interface Direccion {
  departamento: string;
  municipio: string;
  complemento: string;
}

export interface CuerpoDocumentoSujetoExcluido {
  numItem: number;
  tipoItem: number;
  codigo: string;
  descripcion: string;
  cantidad: number;
  uniMedida: number;
  precioUni: number;
  montoDescu: number;
  compra: number;
}

export interface ResumenSujetoExcluido {
  totalCompra: number;
  descu: number;
  totalDescu: number;
  totalPagar: number;
  subTotal: number;
  ivaRete1: number;
  reteRenta: number;
  totalLetras: string;
  condicionOperacion: number;
  pagos: Pago[] | null;
  observaciones: string | null;
}

export interface Pago {
  codigo: string;
  montoPago: number;
  referencia: string | null;
  plazo: string | null;
  periodo: string | null;
}

export interface JsonRespuestaMh {
  version: number;
  ambiente: string;
  versionApp: number;
  estado: string;
  codigoGeneracion: string;
  selloRecibido: string;
  fhProcesamiento: string;
  clasificaMsg: string;
  codigoMsg: string;
  descripcionMsg: string;
  observaciones: any[]; // Puedes tiparlo mejor si sabes su forma
}

export const SujetoExcluidoDefault = {
  tipoDocumento: "",
  numDocumento: "",
  nombre: "",
  codActividad: "",
  descActividad: "",
  correo: "",
  telefono: "",
  direccion: {
    departamento: "",
    municipio: "",
    complemento: "",
  }
}

export const ResumenSujetoExcluidoDefault = {
  totalCompra: 0,
  descu: 0,
  totalDescu: 0,
  totalPagar: 0,
  subTotal: 0,
  ivaRete1: 0,
  reteRenta: 0,
  totalLetras: "",
  condicionOperacion: 0,
  pagos: null,
  observaciones: "",
}