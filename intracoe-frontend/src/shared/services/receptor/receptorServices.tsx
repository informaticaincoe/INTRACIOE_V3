// src/services/receptorService.ts

import { ReceptorInterface } from '../../interfaces/interfaces';
import { api } from '../api';

export const getAllReceptor = async ({
  filter,
}: { filter?: any | null } = {}): Promise<ReceptorInterface[]> => {
  try {
    const params: Record<string, any> = {};
    if (filter) params.filtro = filter;

    const response = await api.get<ReceptorInterface[]>('/receptor/', {
      params,
    });
    return response.data;
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
