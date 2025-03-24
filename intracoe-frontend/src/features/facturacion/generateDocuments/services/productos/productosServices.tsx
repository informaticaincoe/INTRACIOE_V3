import axios from 'axios';
import { ProductoResponse } from '../../../../../shared/interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllProducts = async () => {
  try {
    const response = await axios.get<ProductoResponse[]>(`${BASEURL}/productos/`);
    
    // response.data.map((data)=>{
    //   data.impuestos = 
    // })
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
