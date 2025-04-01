import axios from 'axios';
import { FacturaPorCodigoGeneracionResponse } from '../../../../../shared/interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (data: any) => {
  console.log('data', data);
  try {
    const response = await axios.post(`${BASEURL}/factura/generar/`, data);
    console.log('response generar', response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const generarNotaCreditoService = async (data: any) => {
  console.log('data', data);
  try {
    const response = await axios.post(
      `${BASEURL}/factura_ajuste/generar/`,
      data
    );
    console.log('response generar', response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getFacturaCodigos = async (tipo_dte: string) => {
  try {
    const response = await axios.get(`${BASEURL}/factura/generar/`, {
      params: {
        tipo_dte,
      },
    });
    console.log('response get codigos', response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const FirmarFactura = async (id: string) => {
  try {
    const response = await axios.post(`${BASEURL}/factura/firmar/${id}/`);
    console.log('response firmar factura', response.data);
  } catch (error) {
    console.log(error);
  }
};

export const EnviarHacienda = async (id: string) => {
  try {
    const response = await axios.post(
      `${BASEURL}/factura/enviar_hacienda/${id}/`
    );
    console.log(response);
    return response; // Devuelve si todo bien
  } catch (error) {
    console.error('Error desde EnviarHacienda:', error);
    throw error; // ¡Importante! Propaga el error para que se pueda capturar fuera
  }
};

export const getFacturaBycodigo = async (codigo_generacion: string) => {
  try {
    const response = await axios.get<FacturaPorCodigoGeneracionResponse>(
      `${BASEURL}/factura-por-codigo/`,
      {
        params: {
          codigo_generacion,
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getTiposGeneracionDocumento = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-generacion-facturas/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
