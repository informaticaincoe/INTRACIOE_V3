import axios from 'axios';
import {
  Descuento,
  Impuesto,
  ProductoResponse,
} from '../../interfaces/interfaces';
import { getTributoById } from '../tributos/tributos';

const BASEURLINVENT = import.meta.env.VITE_URL_BASE_INVENT;
const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllProducts = async ({
  filter,
  tipo,
}: {
  filter?: string;
  tipo?: string | number;
} = {}) => {
  // Si no se pasa argumento, se usa un objeto vacío
  try {
    const params: Record<string, any> = {}; // Construimos el objeto `params` sólo con los filtros proporcionados
    if (filter) params.q = filter;
    if (tipo) params.tipo = tipo;

    const response = await axios.get<ProductoResponse[]>(
      `${BASEURLINVENT}/productos/`,
      { params }
    );

    await Promise.all(
      response.data.map(async (data) => {
        data.tributo = await getTributoById(data.tributo);
      })
    );
    return response.data;
  } catch (error) {
    throw new Error('Error fetching products');
  }
};

export const getAllDescuentos = async () => {
  try {
    const response = await axios.get<Descuento[]>(`${BASEURL}/descuento/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllImpuestos = async () => {
  try {
    const response = await axios.get<Impuesto[]>(`${BASEURLINVENT}/impuestos/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllUnidadesDeMedida = async () => {
  try {
    const response = await axios.get(`${BASEURLINVENT}/unidades-medida/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getAllTipoItem = async () => {
  try {
    const response = await axios.get(`${BASEURLINVENT}/tipo-item/`);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
