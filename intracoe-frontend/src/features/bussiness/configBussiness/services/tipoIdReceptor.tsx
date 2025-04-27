import { api } from '../../../../shared/services/api';

export const getAllTipoIdReceptor = async () => {
  try {
    const response = await api.get(`/tipo-id-receptor/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    console.log(error);
  }
};
