import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE_INVENT;

export const getAllTipoTributos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-tributos/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllTributosByTipo = async (id: number) => {
  try {
    const response = await axios.get(`${BASEURL}/tributos/tipo/${id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getTributoById = async (id: number) => {
  try {
    const response = await axios.get(`${BASEURL}/tributo/${id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
