import axios from 'axios';
import { ReceptorInterface } from '../../interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllReceptor = async ({
  filter,
}: { filter?: any | null } = {}) => {
  try {
    const params: Record<string, any> = {}; // Construimos el objeto `params` sólo con los filtros proporcionados
    if (filter) params.filtro = filter;

    const response = await axios.get<ReceptorInterface[]>(
      `${BASEURL}/receptor/`
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getReceptorById = async (id: string) => {
  try {
    const response = await axios.get(`${BASEURL}/receptor/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const tipoIdReceptor = async (id_tipoId: string) => {
  try {
    const response = await axios.get(
      `${BASEURL}/tipo-id-receptor/${id_tipoId}/`
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const deleteReceptor = async (receptor_id: string) => {
  try {
    const response = await axios.delete(
      `${BASEURL}/receptor/eliminar/${receptor_id}/`
    );

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const createReceptor = async (data: any) => {
  try {
    const response = await axios.post(`${BASEURL}/receptor/crear/`, data);

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const editReceptor = async (id: any, data: any) => {
  try {
    const response = await axios.put(
      `${BASEURL}/receptor/actualizar/${id}/`,
      data
    );

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
