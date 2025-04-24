// src/services/dteService.ts
import { TipoDTE } from '../interfaces/interfaces';
import { api } from './api';

export const DTEByCode = async (dte_id: string): Promise<TipoDTE> => {
  try {
    const response = await api.get<TipoDTE>(`/tipo-dte/${dte_id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching DTE with id ${dte_id}:`, error);
    throw new Error('Error fetching DTE by code');
  }
};
