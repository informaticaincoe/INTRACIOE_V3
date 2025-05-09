import {
  Almacen,
  Categoria,
  Impuesto,
  TipoItem,
  TipoUnidadMedida,
} from '../../../../shared/interfaces/interfaces';

export interface ProductosInterfaceResults {
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

export interface ProductosInterface {
  count: number;
  page_size: number;
  current_page: number;
  has_next: boolean;
  has_previous: boolean;
  results: ProductosInterfaceResults[];
}
