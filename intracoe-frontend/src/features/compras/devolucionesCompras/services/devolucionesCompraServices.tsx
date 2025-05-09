import { DevolucionComprasParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import { getProductById } from '../../../inventario/products/services/productsServices';
import { DevolucionCompra } from '../interfaces/devolucionCompraInterfaces';

export const getAllDevolucionesCompra = async (
  { page, limit }: DevolucionComprasParams = {
    page: 1,
    limit: 10,
  }
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<DevolucionCompra>(
      '/devoluciones-compra/',
      {
        params: { page: page, page_size: limit },
      }
    );

    return {
      results: response.data.results,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error: any) {
    console.error(error);
  }
};

export const getDetalleDevolucionCompraById = async (id: string | number) => {
  try {
    const response = await apiInventory.get(
      `/detalle-devolucion-compra/${id}/`
    );
    const detalle = response.data;

    const producto = await getProductById(detalle.producto);
    const detalleConNombre = {
      ...detalle,
      nombreProducto: producto.descripcion,
    };

    return detalleConNombre;
  } catch (error: any) {
    console.error(error);
    return null;
  }
};

export const createDevolucionesCompra = async (data: any) => {
  try {
    const response = await apiInventory.post(
      '/devoluciones-compra/crear/',
      data
    );
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const getAllDetalleDevolucionesCompra = async () => {
  try {
    const response = await apiInventory.get('/detalle-devolucion-compra/');
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};
