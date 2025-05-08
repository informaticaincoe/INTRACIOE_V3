import { AjusteInventarioParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import { getAlmacenById } from '../../../../shared/services/tributos/tributos';
import { getProductById } from '../../products/services/productsServices';
import { AjusteInventarioInterface, AjusteInventarioInterfaceResults } from '../interfaces/ajusteInventarioInterfaces';

export const getAllAjusteInventario = async ({ page, limit }: AjusteInventarioParams = {
  page: 1,
  limit: 10,
}) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<AjusteInventarioInterface>('/ajustes-inventario/', {
      params: { page: page, page_size: limit }
    });

    const data = response.data.results

    const ajusteConNombreProducto = await Promise.all(data.map(async (ajustes) => {
      const producto = await getProductById(ajustes.producto);
      const almacen = await getAlmacenById(ajustes.almacen)
      return {
        ...ajustes,
        nombreProducto: producto.descripcion,
        nombreAlmacen: almacen.nombre
      };
    }));

    return {
      results: ajusteConNombreProducto,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count
    };
  } catch (error: any) {
    console.error(error)
  }
};

export const getAjusteInventarioById = async (id: string | number) => {
  try {
    const response = await apiInventory.get<AjusteInventarioInterface>(`/ajustes-inventario/${id}/`,);
    const data = response.data

    return {
      ...data,
    };
  } catch (error: any) {
    console.error(error)
  }
};

export const addAjusteMovimientoInventario = async (data: any) => {
  try {
    const response = await apiInventory.post<AjusteInventarioInterface>(`/ajustes-inventario/crear/`, data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

// export const updateAjusteInventarioById = async (id: string, data:any) => {
//   try {
//     const response = await apiInventory.put<AjusteInventarioInterface>(`/ajustes-inventario/${id}/editar/`,data);
//     console.log(response.data)
//     return response.data;
//   } catch (error: any) {
//     console.error(error)
//   }
// };

// export const deleteAjusteInventarioById = async (id: string | number) => {
//   try {
//     const response = await apiInventory.delete<AjusteInventarioInterface>(`/ajustes-inventario/${id}/eliminar/`,);
//     console.log(response.data)
//     return response.data;
//   } catch (error: any) {
//     console.error(error)
//   }
// };
