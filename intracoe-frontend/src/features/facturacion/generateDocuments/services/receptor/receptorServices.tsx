import axios from 'axios';
import { ReceptorInterface } from '../../../../../shared/interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllReceptor = async () => {
  try {
    const response = await axios.get<ReceptorInterface[]>(
      `${BASEURL}/receptor/`
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getReceptorById = async (id: number) => {
  try {
    const response = await axios.get(`${BASEURL}/receptor/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const tipoIdReceptor = async (id_tipoId: string) => {
  console.log('id_tipoId', id_tipoId);
  try {
    const response = await axios.get(
      `${BASEURL}/tipo-id-receptor/${id_tipoId}/`
    );
    console.log('RETURN', response.data);

    return response.data;
  } catch (error) {
    console.log(error);
  }
};
