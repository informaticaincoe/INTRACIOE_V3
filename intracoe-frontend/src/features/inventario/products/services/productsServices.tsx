import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE_INVENT;

export const createProductService = async (data: any) => {
  console.log('data', data);
  try {
    const response = await axios.post(`${BASEURL}/productos/crear/`, data); // Usar POST para enviar los datos
    return response.data;
  } catch (error:any) {
    throw new Error(error.response.data.codigo[0]);
  }
};

export const deleteProduct = async (id: any) => {
  try {
    const response = await axios.delete(`${BASEURL}/productos/${id}/eliminar/`); // Usar POST para enviar los datos
    return response.data;
  } catch (error:any) {
    throw new Error(error.response.data.codigo[0]);
  }
};

export const EditProductService = async (id: string, data: any) => {
  console.log('data', data);
  try {
    const response = await axios.put(
      `${BASEURL}/productos/${id}/editar/`,
      data
    ); // Usar POST para enviar los datos
    return response.data;
  } catch (error:any) {
    throw new Error(error.response.data.codigo[0]);
  }
};

export const getProductById = async (id: string) => {
  try {
    const response = await axios.get(`${BASEURL}/productos/${id}/`); // Usar POST para enviar los datos
    return response.data;
  } catch (error:any) {
    throw new Error(error.response.data.codigo[0]);
  }
};
