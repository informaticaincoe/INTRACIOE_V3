import { Contingencias } from '../interfaces/contingenciaInterfaces';
import { api } from '../../../../shared/services/api';

export const GetAlEventosContingencia = async () => {
  try {
    const response = await api.get<Contingencias>(`/contingencia/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    console.log(response.data);
    console.log(response.data.results);

    return response.data;
  } catch (error) {
    console.log(error);
  }
};
