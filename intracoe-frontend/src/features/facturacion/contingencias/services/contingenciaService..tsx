import { Contingencias } from '../interfaces/contingenciaInterfaces';
import { api } from '../../../../shared/services/api';

export const GetAlEventosContingencia = async (page: number) => {
  try {
    const response = await api.get<Contingencias>(`/contingencia/`, {
      params: { page },
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log("rrrrrrrrrrrrrrrr",response.data)
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud de contingencias:', error);
    return null; // Devolver null si ocurre un error
  }
};
