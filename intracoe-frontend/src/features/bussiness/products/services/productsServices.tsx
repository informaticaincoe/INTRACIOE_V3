import axios from 'axios';
import { ProductoRequest } from '../../../../shared/interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE_INVENT;


export const createProductService = async (data: any) => {
    
    console.log("data", data)
    try {
      const response = await axios.post(`${BASEURL}/productos/crear/`, data); // Usar POST para enviar los datos
      return response.data;
    } catch (error) {
      console.log(error);
      throw new Error('Error al crear el producto');
    }
  };
