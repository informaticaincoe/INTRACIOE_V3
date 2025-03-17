import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllDepartamentos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/departamentos/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getMunicipiosByDepartamentos = async (idDepartmento: number) => {
  try {
    const response = await axios.get(`${BASEURL}/municipio/${idDepartmento}/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};
