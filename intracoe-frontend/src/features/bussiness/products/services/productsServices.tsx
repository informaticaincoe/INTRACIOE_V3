import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllUnidadesDeMedida = async () => {
  try {
    const response = await axios.get(`${BASEURL}/unidad-medida/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllTipoItem = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-item/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
