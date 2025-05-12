export interface CompraInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: compraResult[];
}

export interface compraResult {
  id: number;
  proveedor: number;
  nombreProveedor?: string;
  fecha: any;
  total: number;
  estado: string;
}

export interface DetalleCompraPayload {
  id: string | number;
  codigo: string;
  descripcion: string;
  categoria?: number | null;
  unidad_medida?: number | null;
  precio_unitario: string;
  preunitario: string | number;
  precio_venta: string;
  cantidad: string;
  tipo_compra?: string;
  iva_item?: number;
  tipo_item:string;
}

export interface CompraPayload {
  proveedor: any;
  estado: string;
  total: string;
  detalles: DetalleCompraPayload[];
  numero_documento?: string;
  tipo_operacion?: string;
  clasificacion?: string;
  sector?: string;
  tipo_costo_gasto?: number;
}

export const comprarDefault = {
  id: 1,
  proveedor: 123,
  nombreProveedor: 'Proveedor X',
  fecha: new Date(),
  total: 1000,
  estado: 'Pendiente',
};

export const CompraPayloadDeafult = {
  proveedor: 0,
  fecha: new Date(),
  estado: 'Pendiente',
  total: '',
  detalles: [
    {
      id: '0',
      codigo: '',
      descripcion: '',
      categoria: null,
      unidad_medida: null,
      precio_unitario: '',
      preunitario: '',
      precio_venta: '',
      cantidad: '',
      tipo_item:'1'
    },
  ],
};

export const DetalleCompraDefault = {
  id: '0',
  codigo: '',
  descripcion: '',
  categoria: null,
  unidad_medida: null,
  precio_venta: '',
  cantidad: '',
  precio_unitario: '',
  preunitario: '',
  tipo_compra: '',
  iva_item: 0.0,
  tipo_item:"1"
};

export interface Option {
  value: string;
  label: string;
}

export const tipoCompraOptions: Option[] = [
  { value: 'EX_INT', label: 'Interna Exenta' },
  { value: 'EX_INT_NO', label: 'Internaciones Exentas/No Sujetas' },
  { value: 'EX_IMP', label: 'Importaciones Exentas/No Sujetas' },
  { value: 'GR_INT', label: 'Interna Gravada' },
  { value: 'GR_INT_B', label: 'Internaciones Grav. Bienes' },
  { value: 'GR_IMP_B', label: 'Importaciones Grav. Bienes' },
  { value: 'GR_IMP_S', label: 'Importaciones Grav. Servicios' },
];

export const erroresDetalleCompra = {
  codigo: '',
  descripcion: '',
  categoria: '',
  precio_venta: '',
  cantidad: '',
  precio_unitario: '',
  preunitario: '',
};

export const erroresCompra = {
  proveedor: '',
  estado: '',
};

export interface detalleCompraInterfaz {
  cantidad: number;
  compra: number;
  id: number;
  precio_unitario: string;
  subtotal: string;
  producto: number;
  nombreProducto?: string;
  descripcion?: string;
  codigo?: string;
  precio_venta: string;
}
