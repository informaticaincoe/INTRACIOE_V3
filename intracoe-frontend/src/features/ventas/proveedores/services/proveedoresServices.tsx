import { ProveedoressParams } from '../../../../shared/interfaces/interfacesPagination';
import { apiInventory } from '../../../../shared/services/apiInventory';
import { ProveedorInterface, ProveedorResultInterface } from '../interfaces/proveedoresInterfaces';

export const getAllProveedores = async (
  { page, limit }: ProveedoressParams = {
    page: 1,
    limit: 10,
  }
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await apiInventory.get<ProveedorInterface>(
      '/proveedores/',
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

export const getProveedoresById = async (id: string | number) => {
  try {
    const response = await apiInventory.get<ProveedorResultInterface>(
      `/proveedores/${id}/`
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const addProveedor = async (data: any) => {
  try {
    const response = await apiInventory.post<ProveedorInterface>(
      `/proveedores/crear/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const updateProveedoresById = async (id: string, data: any) => {
  try {
    const response = await apiInventory.put<ProveedorInterface>(
      `/proveedores/${id}/editar/`,
      data
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};

export const deleteProveedoresById = async (id: string) => {
  try {
    const response = await apiInventory.delete<ProveedorInterface>(
      `/proveedores/${id}/eliminar/`
    );
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.error(error);
  }
};
