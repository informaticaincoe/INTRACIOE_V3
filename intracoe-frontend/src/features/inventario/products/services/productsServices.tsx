import { apiInventory } from '../../../../shared/services/apiInventory';

export const createProductService = async (data: any) => {
  try {
    const response = await apiInventory.post('/productos/crear/', data);
    return response.data;
  } catch (error: any) {
    const msg =
      error.response?.data?.codigo?.[0] ?? 'Error creando el producto';
    throw new Error(msg);
  }
};

export const deleteProduct = async (id: string) => {
  try {
    const response = await apiInventory.delete(`/productos/${id}/eliminar/`);
    return response.data;
  } catch (error: any) {
    const msg =
      error.response?.data?.codigo?.[0] ?? 'Error eliminando el producto';
    throw new Error(msg);
  }
};

export const editProductService = async (id: string, data: any) => {
  try {
    const response = await apiInventory.put(`/productos/${id}/editar/`, data);
    return response.data;
  } catch (error: any) {
    const msg =
      error.response?.data?.codigo?.[0] ?? 'Error editando el producto';
    throw new Error(msg);
  }
};

export const getProductById = async (id: string | number) => {
  try {
    const response = await apiInventory.get(`/productos/${id}/`);
    return response.data;
  } catch (error: any) {
    const msg =
      error.response?.data?.codigo?.[0] ?? 'Error obteniendo el producto';
    throw new Error(msg);
  }
};
