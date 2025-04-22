export interface FacturaResponse {
  id: number;
  detalles: number[];
  version: string;
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
  formas_Pago: any; // Puede reemplazarse con una interfaz concreta si se conoce
  firmado: boolean;
  json_original: JsonOriginal;
  json_firmado: any; // Según implementación
  sello_recepcion: any; // Según implementación
  recibido_mh: boolean;
  estado: boolean;
  base_imponible: boolean;
  tipo_dte: number;
  tipomodelo: number;
  tipocontingencia: any; // Según implementación
  tipomoneda: number;
  dteemisor: number;
  dtereceptor: number;
  condicion_operacion: number;
}

export interface TipoIdentificacion {
  id: number;
  codigo: string;
  descripcion: string;
}
export interface JsonOriginal {
  identificacion: Identificacion;
  documentoRelacionado: any;
  emisor: Emisor;
  receptor: Receptor;
  otrosDocumentos: any;
  ventaTercero: any;
  cuerpoDocumento: CuerpoDocumento[];
  resumen: Resumen;
  extension: Extension;
  apendice: any;
}

export interface Identificacion {
  version: number;
  ambiente: string;
  tipoDte: string;
  numeroControl: string;
  codigoGeneracion: string;
  tipoModelo: number;
  tipoOperacion: number;
  tipoContingencia: any;
  motivoContin: any;
  fecEmi: string;
  horEmi: string;
  tipoMoneda: string;
}

export interface Emisor {
  nit: string;
  nrc: string;
  nombre: string;
  codActividad: string;
  descActividad: string;
  nombreComercial: string;
  tipoEstablecimiento: string;
  direccion: Direccion;
  telefono: string;
  correo: string;
  codEstableMH: string;
  codEstable: string;
  codPuntoVentaMH: string;
  codPuntoVenta: string;
}

export const EmisorDefault = {
  nit: '',
  nrc: '',
  nombre: '',
  codActividad: '',
  descActividad: '',
  nombreComercial: '',
  tipoEstablecimiento: '',
  direccion: {
    departamento: '',
    municipio: '',
    complemento: '',
  },
  telefono: '',
  correo: '',
  codEstableMH: '',
  codEstable: '',
  codPuntoVentaMH: '',
  codPuntoVenta: '',
};

export const ReceptorDefault = {
  nombre: '',
  codActividad: '',
  descActividad: '',
  direccion: {
    departamento: '',
    municipio: '',
    complemento: '',
  },
  telefono: '',
  correo: '',
  nrc: null,
  tipoDocumento: '',
  numDocumento: '',
};
export interface Receptor {
  nombre: string;
  codActividad: string;
  descActividad: string;
  direccion: Direccion;
  telefono: string;
  correo: string;
  nrc: string | null;
  tipoDocumento?: string;
  numDocumento?: string;
  nit?: string;
}

export interface Direccion {
  departamento: string;
  municipio: string;
  complemento: string;
}

export const CuerpoDocumentoDefault = [
  {
    numItem: 0,
    tipoItem: 0,
    numeroDocumento: '',
    codigo: '',
    codTributo: '',
    descripcion: '',
    cantidad: 0,
    uniMedida: 0,
    precioUni: 0,
    montoDescu: 0,
    ventaNoSuj: 0,
    ventaExenta: 0,
    ventaGravada: 0,
    tributos: '',
    psv: 0,
    noGravado: 0,
    ivaItem: 0,
  },
];
export interface CuerpoDocumento {
  numItem: number;
  tipoItem: number;
  numeroDocumento: string | null;
  codigo: string;
  codTributo: string | null;
  descripcion: string;
  cantidad: number;
  uniMedida: number;
  precioUni: number;
  montoDescu: number;
  ventaNoSuj: number;
  ventaExenta: number;
  ventaGravada: number;
  tributos: any;
  psv: number;
  noGravado: number;
  ivaItem: number;
}

export const ResumenDefalt = {
  totalNoSuj: 0,
  totalExenta: 0,
  totalGravada: 0,
  subTotalVentas: 0,
  descuNoSuj: 0,
  descuExenta: 0,
  descuGravada: 0,
  porcentajeDescuento: 0,
  totalDescu: 0,
  subTotal: 0,
  ivaRete1: 0,
  reteRenta: 0,
  montoTotalOperacion: 0,
  totalNoGravado: 0,
  totalPagar: 0,
  totalLetras: '',
  saldoFavor: 0,
  condicionOperacion: '',
  pagos: [],
  numPagoElectronico: '',
  tributos: '',
  totalIva: 0,
};

export const resumenTablaFEDefault = {
  totalNoSuj: '',
  totalExenta: '',
  totalGravada: '',
  subTotalVentas: '',
  descuNoSuj: '',
  descuExenta: '',
  descuGravada: '',
  porcentajeDescuento: '',
  totalDescu: '',
  subTotal: '',
  ivaRete: '',
  reteRenta: '',
  montoTotalOperacion: '',
  totalNoGravado: '',
  totalPagar: '',
  totalLetras: '',
  saldoFavor: '',
  condicionOperacion: 0,
  pagos: [],
  numPagoElectronico: '',
  tributos: '',
  totalIva: '',
};
export interface Resumen {
  totalNoSuj: string;
  totalExenta: string;
  totalGravada: string;
  subTotalVentas: string;
  descuNoSuj: string;
  descuExenta: string;
  descuGravada: string;
  porcentajeDescuento: string;
  totalDescu: string;
  subTotal: string;
  ivaRete: string;
  reteRenta: string;
  montoTotalOperacion: string;
  totalNoGravado: string;
  totalPagar: string;
  totalLetras: string;
  saldoFavor: string | null;
  condicionOperacion: number;
  pagos: any[];
  numPagoElectronico: string | null;
  tributos: any;
  totalIva: string;
}

export const ExtensionDefault = {
  nombEntrega: '',
  docuEntrega: '',
  nombRecibe: '',
  docuRecibe: '',
  observaciones: '',
  placaVehiculo: '',
};

export interface Extension {
  nombEntrega: string | null;
  docuEntrega: string | null;
  nombRecibe: string | null;
  docuRecibe: string | null;
  observaciones: string;
  placaVehiculo: string | null;
}

export const DatosFacturaDefault = {
  tipoDte: '',
  codigoGeneracion: '',
  numeroControl: '',
  fechaEmision: '',
  horaEmision: '',
  selloRemision: '',
};
export interface DatosFactura {
  tipoDte: string;
  codigoGeneracion: string;
  numeroControl: string;
  fechaEmision: string;
  horaEmision: string;
  selloRemision: string;
}
