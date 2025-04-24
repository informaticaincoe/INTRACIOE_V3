import axios from 'axios';
import { ActivitiesDataNew } from '../../../../shared/interfaces/interfaces';
import { api } from '../../../../shared/services/api';

export const createActivity = async (activity: ActivitiesDataNew) => {
  console.log('activity', activity);
  try {
    const response = await api.post(`/actividad/crear/`, activity, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response;
  } catch (error) {
    console.log(error);
  }
};

export const deleteActivity = async (id: number) => {
  try {
    const response = await api.delete(`/actividad/eliminar/${id}/`);
    console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
};
