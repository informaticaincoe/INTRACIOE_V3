
import {
  Descuento,
  Impuesto,
  ProductoResponse,
} from '../../interfaces/interfaces';
import { api } from '../api';
import { apiInventory } from '../apiInventory';
import { getTributoById } from '../tributos/tributos';

export const getAllProducts = async ({
  filter,
  tipo,
}: {
  filter?: string;
  tipo?: string | number;
} = {}) => {
  try {
    const params: Record<string, any> = {};
    if (filter) params.q = filter;
    if (tipo) params.tipo = tipo;

    const response = await apiInventory.get<ProductoResponse[]>(
      '/productos/',
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
    const response = await api.get<Descuento[]>('/descuento/');
    return response.data;
  } catch (error) {
    throw new Error('Error fetching descuentos');
  }
};

export const getAllImpuestos = async () => {
  try {
    const response = await apiInventory.get<Impuesto[]>('/impuestos/');
    return response.data;
  } catch (error) {
    throw new Error('Error fetching impuestos');
  }
};

export const getAllUnidadesDeMedida = async () => {
  try {
    const response = await apiInventory.get('/unidades-medida/');
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Error fetching unidades de medida');
  }
};

export const getAllTipoItem = async () => {
  try {
    const response = await apiInventory.get('/tipo-item/');
    return response.data;
  } catch (error) {
    console.error(error);
    throw new Error('Error fetching tipo de item');
  }
};
