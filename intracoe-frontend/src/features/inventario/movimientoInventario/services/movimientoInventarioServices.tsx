import { apiInventory } from '../../../../shared/services/apiInventory';
import { getAllAlmacenes, getAlmacenById } from '../../../../shared/services/tributos/tributos';
import { getProductById } from '../../products/services/productsServices';
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface';

export const getAllMovimientosInventario = async () => {
  try {
    const response = await apiInventory.get<movimientoInterface[]>('/movimientos-inventario/',);
    const movimientos = response.data;

    const movimientosConNombreProducto = await Promise.all(movimientos.map(async (movimiento) => {
      const producto = await getProductById(movimiento.producto);
      const almacen = await getAlmacenById(movimiento.almacen)
      return {
        ...movimiento,
        nombreProducto: producto.descripcion,
        nombreAlmacen: almacen.nombre
      };
    }));

    console.log(movimientosConNombreProducto);
    return movimientosConNombreProducto;
  } catch (error: any) {
    console.error(error)
  }
};

export const getMovimientosInventarioById = async (id: string | number) => {
  try {
    const response = await apiInventory.get<movimientoInterface>(`/movimientos-inventario/${id}/`,);

    const data = response.data

    const nombreProducto = await getProductById(data.producto)
    const nombreAlmacen = await getAlmacenById(data.almacen)

  
    return {
      ...data,
      nombreProducto: nombreProducto.descripcion,
      nombreAlmacen: nombreAlmacen.nombre

    };
  } catch (error: any) {
    console.error(error)
  }
};

export const addMovimientoInventario = async (data:any) => {
  try {
    const response = await apiInventory.post<movimientoInterface>(`/movimientos-inventario/crear/`,data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const updateMovimientosInventarioById = async (id: string, data:any) => {
  try {
    const response = await apiInventory.put<movimientoInterface>(`/movimientos-inventario/${id}/editar/`,data);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};

export const deleteMovimientosInventarioById = async (id: string | number) => {
  try {
    const response = await apiInventory.delete<movimientoInterface>(`/movimientos-inventario/${id}/eliminar/`,);
    console.log(response.data)
    return response.data;
  } catch (error: any) {
    console.error(error)
  }
};
