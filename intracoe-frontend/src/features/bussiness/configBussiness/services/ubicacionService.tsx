import { api } from "../../../../shared/services/api";


export const getAllDepartamentos = async () => {
  try {
    const response = await api.get(`/departamentos/`, {
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
    const response = await api.get(`/municipios/departamento/${idDepartmento}/`, {
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

export const getMunicipiosById = async (id: string) => {
  try {
    const response = await api.get(`/municipio-by-id/${id}/`, {
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