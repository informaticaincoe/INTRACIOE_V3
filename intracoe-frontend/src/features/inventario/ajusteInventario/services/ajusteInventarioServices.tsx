import { apiInventory } from '../../../../shared/services/apiInventory';
import { getAlmacenById } from '../../../../shared/services/tributos/tributos';
import { getProductById } from '../../products/services/productsServices';
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces';

export const getAllAjusteInventario = async () => {
  try {
    const response = await apiInventory.get<AjusteInventarioInterface[]>('/ajustes-inventario/',);
    const data = response.data

    const ajusteConNombreProducto = await Promise.all(data.map(async (ajustes) => {
      const producto = await getProductById(ajustes.producto);
      const almacen = await getAlmacenById(ajustes.almacen)
      return {
        ...ajustes,
        nombreProducto: producto.descripcion,
        nombreAlmacen: almacen.nombre
      };
    }));

    console.log(ajusteConNombreProducto);
    return ajusteConNombreProducto;
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
