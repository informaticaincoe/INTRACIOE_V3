import axios from 'axios';
import { FacturaPorCodigoGeneracionResponse } from '../../../../../shared/interfaces/interfaces';
import { ProductosTabla } from '../../components/FE/productosAgregados/productosData';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (data: any) => {
  try {
    const response = await axios.post(`${BASEURL}/factura/generar/`, data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const generarAjusteService = async () => {
  try {
    const response = await axios.get(`${BASEURL}/factura_ajuste/generar/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const generarNotaCreditoService = async (data: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/factura_ajuste/generar/`,
      data
    );
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
    const productosConExtras: ProductosTabla[] = response.data.productos.map(
      (p: ProductosTabla) => ({
        ...p,
        cantidad: 1,
        descuento: 0,
        iva_unitario: 0,
        iva_percibido: 0,
        total_neto: 0,
        total_iva: 0,
        total_con_iva: 0,
        total_tributos: 0,
        seleccionar: false,
      })
    );

    return {
      ...response.data,
      producto: productosConExtras,
    };
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const FirmarFactura = async (id: string) => {
  try {
    const response = await axios.post(`${BASEURL}/factura/firmar/${id}/`);
  } catch (error) {
    console.log(error);
  }
};

export const EnviarHacienda = async (id: string) => {
  try {
    const response = await axios.post(
      `${BASEURL}/factura/enviar_hacienda/${id}/`
    );
    return response;
  } catch (error) {
    console.error('Error desde EnviarHacienda:', error);
    throw error;
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
