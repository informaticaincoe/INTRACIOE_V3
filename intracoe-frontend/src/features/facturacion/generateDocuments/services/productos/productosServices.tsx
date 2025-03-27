import axios from 'axios';
import { Descuento, ProductoResponse } from '../../../../../shared/interfaces/interfaces';
import { getTributoById } from '../tributos/tributos';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllProducts = async () => {
  try {
    const response = await axios.get<ProductoResponse[]>(`${BASEURL}/productos/`);
    await Promise.all(response.data.map(async (data) => {
      data.tributo = await getTributoById(data.tributo)
    }));
    console.log("response.data", response.data)
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDescuentos = async () => {
  try {
    const response = await axios.get<Descuento[]>(`${BASEURL}/descuentos/`);
    console.log("response.data", response.data)
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
