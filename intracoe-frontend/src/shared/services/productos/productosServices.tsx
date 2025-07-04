import { ProductosInterface } from '../../../features/inventario/products/interfaces/productosInterfaces';
import { Descuento, Impuesto } from '../../interfaces/interfaces';
import { ProductosParams } from '../../interfaces/interfacesPagination';
import { api } from '../api';
import { apiInventory } from '../apiInventory';
import { getTributoById } from '../tributos/tributos';

export const getAllProducts = async (
  { filter, tipo, page, limit }: ProductosParams = {
    page: 1,
    limit: 10,
  }
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<ProductosInterface>('/productos/', {
      params: { q: filter, tipo: tipo, page: page, page_size: limit },
    });

    const data = response.data.results;

    await Promise.all(
      data.map(async (data) => {
        data.tributo = await getTributoById(data.tributo);
      })
    );

    return {
      results: data,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error) {
    throw new Error('Error fetching products');
  }
};

export const getAllDescuentos = async () => {
  try {
    const response = await api.get<Descuento[]>('/descuento/');
    return response.data;
  } catch (error) {
    throw new Error('Error fetching descuentos');
  }
};

export const getAllImpuestos = async () => {
  try {
    const response = await apiInventory.get<Impuesto[]>('/impuestos/');
    return response.data;
  } catch (error) {
    throw new Error('Error fetching impuestos');
  }
};

export const getAllUnidadesDeMedida = async () => {
  try {
    const response = await apiInventory.get('/unidades-medida/');
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Error fetching unidades de medida');
  }
};

export const getAllTipoItem = async () => {
  try {
    const response = await apiInventory.get('/tipo-item/');
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Error fetching tipo de item');
  }
};

/*************************** PRODCUTOS POR PROVEEDOR ***************************/
export const getProductosProveedores = async (id: any, { page, limit }: ProductosParams = {
  page: 1,
  limit: 10,
}) => {

  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));


  try {
    const response = await apiInventory.get(`/proveedor/${id}/productos/`,
      { params: { page: page, page_size: limit }, }
    )
    console.log("RESPONSE DATA", response.data)
  
    const data = response.data.results.map((producto: any) => ({
      ...producto,
      cantidad: 0,
      descuento: 0,
    }));

    return {
      results: data,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  }
  catch (error) {
    console.log(error)
  }
}