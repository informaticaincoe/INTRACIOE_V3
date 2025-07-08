import axios from 'axios';
import { Almacen } from '../../interfaces/interfaces';
import { apiInventory } from '../apiInventory';

export const getAllTipoTributos = async (): Promise<any[]> => {
  try {
    const response = await apiInventory.get('/tipo-tributos/');
    return response.data;
  } catch (error) {
    console.error('Error fetching tipo-tributos:', error);
    throw new Error('Error fetching tipo de tributos');
  }
};

/**
 * Obtiene los tributos de un tipo específico
 * @param id Identificador del tipo de tributo
 */
export const getAllTributosByTipo = async (id: number): Promise<any[]> => {
  try {
    const response = await apiInventory.get(`/tributos/tipo/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tributos for tipo ${id}:`, error);
    throw new Error('Error fetching tributos by tipo');
  }
};

/**
 * Obtiene un tributo por su ID
 * @param id Identificador del tributo
 */
export const getTributoById = async (id: number): Promise<any> => {
  try {
    const response = await apiInventory.get(`/tributo/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching tributo ${id}:`, error);
    throw new Error('Error fetching tributo by ID');
  }
};

/**
 * Obtiene todos los tributos disponibles
 */
export const getAllTributos = async (): Promise<any[]> => {
  try {
    const response = await apiInventory.get('/tributo/');
    return response.data;
  } catch (error) {
    console.error('Error fetching all tributos:', error);
    throw new Error('Error fetching tributos');
  }
};

/**
 * Obtiene el listado de almacenes
 */
export const getAllAlmacenes = async (): Promise<any[]> => {
  try {
    const response = await apiInventory.get('/almacenes/');
    return response.data;
  } catch (error) {
    console.error('Error fetching almacenes:', error);
    throw new Error('Error fetching almacenes');
  }
};

export const getAlmacenById = async (
  id: string | number,
  signal?: AbortSignal
) => {
  try {
    const response = await apiInventory.get(`/almacenes/${id}/`, { signal });
    return response.data;
  } catch (error: any) {
    if (axios.isCancel(error)) {
      console.log('Petición cancelada (almacén)', error.message);
      return null;
    }
    throw new Error('Error obteniendo el almacén');
  }
};

