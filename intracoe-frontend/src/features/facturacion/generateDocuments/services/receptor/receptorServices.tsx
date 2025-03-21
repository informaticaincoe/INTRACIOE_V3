import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllReceptor = async () => {
  try {
    const response = await axios.get(`${BASEURL}/receptor/`);
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