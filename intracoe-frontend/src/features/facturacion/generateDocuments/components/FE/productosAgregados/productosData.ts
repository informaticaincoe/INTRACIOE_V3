import { Descuento } from '../../../../../../shared/interfaces/interfaces';

export interface ProductosTabla {
  // Campos de base de datos
  id: number;
  codigo: string;
  descripcion: string;
  imagen: string;
  categoria_id: number | null;
  tipo_item_id: number | null;
  unidad_medida_id: number;
  tributo_id: number;
  referencia_interna: string;
  maneja_lotes: boolean;
  fecha_vencimiento: string | null;
  creado: string;
  actualizado: string;
  precio_compra: number;
  precio_venta: number;
  preunitario: number;
  precio_iva: boolean;
  stock: number;
  stock_minimo: number;
  stock_maximo: number;
  seleccionar: boolean;

  // // Campos calculados / de UI
  cantidad: number;
  descuento: Descuento | null;
  iva_unitario: number;
  iva_percibido: number;
  total_neto: number;
  total_iva: number;
  total_con_iva: number;
  total_tributos: number;
}

export const defaultProductosData = {
  id: 0,
  codigo: '',
  descripcion: '',
  preciounitario: 0,
  cantidad: 0,
  no_grabado: false,
  descuento: null,
  iva_unitario: 0,
  total_neto: 0,
  total_iva: 0,
  total_con_iva: 0,
  iva_percibido: 0,
  total_tributos: 0,
  seleccionar: false,
};
