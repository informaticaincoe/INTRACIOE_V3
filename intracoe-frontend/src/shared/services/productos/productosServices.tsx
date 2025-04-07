import axios from 'axios';
import { Descuento, Impuesto, ProductoResponse } from '../../interfaces/interfaces';
import { getTributoById } from '../tributos/tributos';

const BASEURL = import.meta.env.VITE_URL_BASE_INVENT;

export const getAllProducts = async () => {
  try {
    const response = await axios.get<ProductoResponse[]>(
      `${BASEURL}/productos/`
    );
    await Promise.all(
      response.data.map(async (data) => {
        data.tributo = await getTributoById(data.tributo);
      })
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDescuentos = async () => {
  try {
    const response = await axios.get<Descuento[]>(`${BASEURL}/descuentos/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllImpuestos = async () => {
  try {
    const response = await axios.get<Impuesto[]>(`${BASEURL}/impuestos/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
}

export const getAllUnidadesDeMedida = async () => {
  try {
    const response = await axios.get(`${BASEURL}/unidad-medida/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllTipoItem = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-item/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};