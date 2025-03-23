import axios from 'axios';
import { ActivitiesDataNew } from '../../../../shared/interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllActivities = async () => {
  try {
    // Asegúrate de que el endpoint sea el correcto
    const response = await axios.get(
      'http://127.0.0.1:8000/api/api/actividad/'
    );
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const createActivity = async (activity: ActivitiesDataNew) => {
  console.log("activity", activity)
  try {
    const response = await axios.post(`${BASEURL}/actividad/crear/`, activity, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response;
  } catch (error) {
    console.log(error);
  }
};

export const updateActivity = async (
  id: number,
  activity: ActivitiesDataNew
) => {
  console.log('activity:', typeof activity);
  console.log('activity element:', activity);

  try {
    const response = await axios.put(
      `${BASEURL}/actividad/actualizar/${id}/`,
      activity,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
};

export const deleteActivity = async (id: number) => {
  try {
    const response = await axios.delete(`${BASEURL}/actividad/eliminar/${id}/`);
    console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
};
