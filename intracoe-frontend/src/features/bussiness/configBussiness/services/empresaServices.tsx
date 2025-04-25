// src/services/empresaService.ts

import { RequestEmpresa } from '../../../../shared/interfaces/interfaces';
import { api } from '../../../../shared/services/api';

export const getAllEmpresas = async (): Promise<RequestEmpresa[]> => {
  try {
    const response = await api.get<RequestEmpresa[]>('/emisor/');
    return response.data;
  } catch (error) {
    console.error('Error fetching empresas:', error);
    throw new Error('Error fetching empresas');
  }
};

export const getEmpresaById = async (id: number): Promise<RequestEmpresa> => {
  try {
    const response = await api.get<RequestEmpresa>(`/emisor/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching empresa ${id}:`, error);
    throw new Error('Error fetching empresa');
  }
};

export const createEmpresa = async (
  data: RequestEmpresa
): Promise<RequestEmpresa> => {
  try {
    const response = await api.post<RequestEmpresa>('/emisor/crear/', data);
    return response.data;
  } catch (error: any) {
    console.error('Error creating empresa:', error);
    throw new Error(error.response?.data?.detail || 'Error creating empresa');
  }
};

export const editEmpresa = async (
  id: string,
  data: Partial<RequestEmpresa>
): Promise<RequestEmpresa> => {
  try {
    const response = await api.put<RequestEmpresa>(
      `/emisor/editar/${id}/`,
      data
    );
    return response.data;
  } catch (error: any) {
    console.error(`Error updating empresa ${id}:`, error);
    throw new Error(error.response?.data?.detail || 'Error updating empresa');
  }
};

export const getCodigoEstablecimientoById = async (
  idEstablecimiento: number
): Promise<string> => {
  try {
    // Ajusta la ruta y payload según tu API si fuera distinto
    const response = await api.post<{ codigo: string }>(
      '/emisor/codigo-establecimiento/',
      { id: idEstablecimiento }
    );
    return response.data.codigo;
  } catch (error) {
    console.error(
      `Error fetching código de establecimiento ${idEstablecimiento}:`,
      error
    );
    throw new Error('Error fetching código de establecimiento');
  }
};
