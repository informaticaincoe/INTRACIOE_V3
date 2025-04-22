import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE_INVENT;
const BASEURLINVENT = import.meta.env.VITE_URL_BASE_INVENT;

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
    const response = await axios.get(`${BASEURLINVENT}/tributo/${id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllTributos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tributo/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllAlmacenes = async () => {
  try {
    const response = await axios.get(`${BASEURL}/almacenes/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
