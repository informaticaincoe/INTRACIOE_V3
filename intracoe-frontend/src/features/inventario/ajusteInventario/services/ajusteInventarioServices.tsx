import { apiInventory } from '../../../../shared/services/apiInventory';
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces';

export const getAllAjusteInventario = async () => {
  try {
    const response = await apiInventory.get<AjusteInventarioInterface[]>('/ajustes-inventario/',);

    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

// export const getAjusteInventarioById = async (id: string | number) => {
//   try {
//     const response = await apiInventory.get<AjusteInventarioInterface>(`/ajustes-inventario/${id}/`,);

//     const data = response.data

//     const nombreProducto = await getProductById(data.producto)
//     const nombreAlmacen = await getAlmacenById(data.almacen)

  
//     return {
//       ...data,
//       nombreProducto: nombreProducto.descripcion,
//       nombreAlmacen: nombreAlmacen.nombre

//     };
//   } catch (error: any) {
//     console.error(error)
//   }
// };

// export const addAjusteMovimientoInventario = async (data:any) => {
//   try {
//     const response = await apiInventory.post<AjusteInventarioInterface>(`/ajustes-inventario/crear/`,data);
//     console.log(response.data)
//     return response.data;
//   } catch (error: any) {
//     console.error(error)
//   }
// };

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
