import { DevolucionComprasParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import { getProductById } from '../../../inventario/products/services/productsServices';
import { DevolucionCompra } from '../interfaces/devolucionCompraInterfaces';

interface PaginatedResponse<T> {
  results: T[];
  current_page: number;
  page_size: number;
  has_next: boolean;
  has_previous: boolean;
  count: number;
}

export const getAllDevolucionesCompra = async (
  { page, limit }: DevolucionComprasParams = { page: 1, limit: 10 }
): Promise<PaginatedResponse<DevolucionCompra>> => {
  try {
    const response = await apiInventory.get<PaginatedResponse<DevolucionCompra>>(
      '/devoluciones-compra/',
      { params: { page, page_size: limit } }
    );
    const data = response.data.results
    // por cada devolución, recorremos sus detalles y traemos el nombre del producto
    const resultsWithNames = await Promise.all(
      data.map(async (devolucion: any) => {
        const detallesConNombre = await Promise.all(
          devolucion.detalles_creados.map(async (detalle: any) => {
            // suponiendo que tu endpoint de producto a detalle es /productos/:id/
            const prodResp = await getProductById(detalle.producto)
            console.log(prodResp)
            return {
              ...detalle,
              nombreProducto: prodResp.descripcion, // o el campo que uses para el nombre
            };
          })
        );
        return {
          ...devolucion,
          detalles_creados: detallesConNombre,
        };
      })
    );
    console.log("resultsWithNames", resultsWithNames)
    return {
      results: resultsWithNames,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error: any) {
    console.error('Error fetching devoluciones:', error);
    throw error;
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

    console.log(detalleConNombre)

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
