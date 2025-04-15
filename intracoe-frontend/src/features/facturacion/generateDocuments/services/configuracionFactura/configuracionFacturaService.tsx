import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllTipoDte = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-dte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllCondicionDeOperacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/condicion-operacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getCondicionDeOperacionById = async (id: number) => {
  try {
    const response = await axios.get(`${BASEURL}/condicion-operacion/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
