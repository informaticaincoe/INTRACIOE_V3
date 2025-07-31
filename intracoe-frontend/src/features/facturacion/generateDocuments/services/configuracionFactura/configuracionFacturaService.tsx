import { api } from '../../../../../shared/services/api';

export const getAllTipoDte = async () => {
  try {
    const response = await api.get(`/tipo-dte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllCondicionDeOperacion = async () => {
  try {
    const response = await api.get(`/condicion-operacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getCondicionDeOperacionById = async (id: number) => {
  console.log("IDDDDDDDDDDD",id)
  try {
    const response = await api.get(`/condicion-operacion/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getTipoContingencia = async () => {
  try {
    const response = await api.get(`/tipo-contingencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
