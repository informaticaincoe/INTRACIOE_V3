import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllTiposEstablecimientos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-establecimiento/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};
