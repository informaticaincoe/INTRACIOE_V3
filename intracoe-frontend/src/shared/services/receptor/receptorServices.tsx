// src/services/receptorService.ts

import { ReceptorInterface } from '../../../features/ventas/receptores/interfaces/receptorInterfaces';
import { ReceptoresParams } from '../../interfaces/interfacesPagination';
import { api } from '../api';

export const getAllReceptor = async ({
  filter, page, limit

}: ReceptoresParams = {
    page: 1,
    limit: 10,
  }) => {
  try {

    const queryParams = new URLSearchParams();

    //paginacion
    queryParams.append('page', String(page));
    queryParams.append('page_size', String(limit));

    const response = await api.get<ReceptorInterface>('/receptor/', {
      params: { page: 1, page_size: limit, filter: filter }
    });

    return {
      results: response.data.results,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count
    };
  } catch (error) {
    console.error('Error fetching receptores:', error);
    throw new Error('Error fetching receptores');
  }
};

export const getReceptorById = async (
  id: string
): Promise<ReceptorInterface> => {
  try {
    const response = await api.get<ReceptorInterface>(`/receptor/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching receptor ${id}:`, error);
    throw new Error('Error fetching receptor');
  }
};

export const tipoIdReceptor = async (id_tipoId: string): Promise<any> => {
  try {
    const response = await api.get(`/tipo-id-receptor/${id_tipoId}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tipo-id-receptor ${id_tipoId}:`, error);
    throw new Error('Error fetching tipo de identificación');
  }
};

export const deleteReceptor = async (receptor_id: string): Promise<any> => {
  try {
    const response = await api.delete(`/receptor/eliminar/${receptor_id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting receptor ${receptor_id}:`, error);
    throw new Error('Error deleting receptor');
  }
};

export const createReceptor = async (
  data: ReceptorInterface
): Promise<ReceptorInterface> => {
  try {
    const response = await api.post<ReceptorInterface>(
      '/receptor/crear/',
      data
    );
    return response.data;
  } catch (error) {
    console.error('Error creating receptor:', error);
    throw new Error('Error creating receptor');
  }
};

export const editReceptor = async (
  id: string,
  data: ReceptorInterface
): Promise<ReceptorInterface> => {
  try {
    const response = await api.put<ReceptorInterface>(
      `/receptor/actualizar/${id}/`,
      data
    );
    return response.data;
  } catch (error) {
    console.error(`Error updating receptor ${id}:`, error);
    throw new Error('Error updating receptor');
  }
};
