import axios from 'axios'

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllEmpresas = async () => {
  console.log(BASEURL)
  try {
    const response = await axios.get(`${BASEURL}/emisor/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getEmpresaById = (id: number) => {
  console.log(id);
};

export const createEmpresaById = async (data: any) => {
  try {
    const response = await axios.post(`${BASEURL}/emisor/crear/`, data, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    console.log(response);
    return response;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getCodigoEstablecimientoById = async(idEstablecimiento: any) => {
  try {
    const response = await axios.post(`${BASEURL}/emisor/crear/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
  } catch (error) {
    throw new Error();
  }
}
