import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const DTEByCode = async (dte_id: string) => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-dte/${dte_id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
