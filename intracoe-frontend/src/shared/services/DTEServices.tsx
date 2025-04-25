// src/services/dteService.ts
import { TipoDTE } from '../interfaces/interfaces';
import { api } from './api';

export const DTEByCode = async (dte_code: string): Promise<TipoDTE> => {
  try {
    const response = await api.get<TipoDTE>(`/tipo-dte/${dte_code}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching DTE with id ${dte_code}:`, error);
    throw new Error('Error fetching DTE by code');
  }
};
