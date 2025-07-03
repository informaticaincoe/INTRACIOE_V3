import axios from 'axios';
import { MovimientoInventarioParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import {
  getAllAlmacenes,
  getAlmacenById,
} from '../../../../shared/services/tributos/tributos';
import { getProductById } from '../../products/services/productsServices';
import {
  movimientoInterface,
  resultsMovimiento,
} from '../interfaces/movimientoInvetarioInterface';

export const getAllMovimientosInventario = async (
  { page, limit }: MovimientoInventarioParams = {
    page: 1,
    limit: 10,
  },
  signal?: AbortSignal
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<movimientoInterface>(
      '/movimientos-inventario/',
      {
        params: { page, page_size: limit },
        signal,
      }
    );
    const movimientos = response.data.results;
    console.log(response.data);

    const movimientosConNombreProducto = await Promise.all(
      movimientos.map(async (movimiento: any) => {
        const producto = await getProductById(movimiento.producto);
        const almacen = await getAlmacenById(movimiento.almacen);
        return {
          ...movimiento,
          nombreProducto: producto.descripcion,
          nombreAlmacen: almacen.nombre,
        };
      })
    );

    console.log(movimientosConNombreProducto);
    console.log('API RESPONSE DATA', response.data);
    return {
      results: movimientosConNombreProducto,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error: any) {
    if (axios.isCancel(error)) {
      console.log("Petición cancelada");
    } else {
      console.error(error);
    }
  }
};

export const getMovimientosInventarioById = async (id: string | number) => {
  try {
    const response = await apiInventory.get<resultsMovimiento>(
      `/movimientos-inventario/${id}/`
    );

    const data = response.data;

    const nombreProducto = await getProductById(data.producto);
    const nombreAlmacen = await getAlmacenById(data.almacen);

    return {
      ...data,
      nombreProducto: nombreProducto.descripcion,
      nombreAlmacen: nombreAlmacen.nombre,
    };
  } catch (error: any) {
    console.error(error);
  }
};

export const addMovimientoInventario = async (data: any) => {
  try {
    const response = await apiInventory.post<movimientoInterface>(
      `/movimientos-inventario/crear/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const updateMovimientosInventarioById = async (
  id: string,
  data: any
) => {
  try {
    const response = await apiInventory.put<movimientoInterface>(
      `/movimientos-inventario/${id}/editar/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const deleteMovimientosInventarioById = async (id: string | number) => {
  try {
    const response = await apiInventory.delete<movimientoInterface>(
      `/movimientos-inventario/${id}/eliminar/`
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};
