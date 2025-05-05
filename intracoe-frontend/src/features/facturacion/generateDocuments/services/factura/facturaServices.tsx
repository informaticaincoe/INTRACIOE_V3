import { FacturaPorCodigoGeneracionResponse } from '../../../../../shared/interfaces/interfaces';
import { api } from '../../../../../shared/services/api';
import { ProductosTabla } from '../../components/FE/productosAgregados/productosData';

export const generarFacturaService = async (data: any) => {
  try {
    const response = await api.post(`/factura/generar/`, data);
    return response.data;
  } catch (error: any) {
    console.log('ERROR:', error.response.data);
    throw new Error();
  }
};

export const generarAjusteService = async (data: string) => {
  console.log("data", data)
  try {
    const response = await api.get(`/factura_ajuste/generar/`, {
      params: {
        data,
      },
    });

    return response.data;
  } catch (error: any) {
    console.log('ERROR:', error.response.data);

    throw new Error();
  }
};

export const generarNotaCreditoService = async (data: any) => {
  try {
    const response = await api.post(`/factura_ajuste/generar/`, data);
    return response.data;
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const getFacturaCodigos = async (tipo_dte: string) => {
  try {
    const response = await api.get(`/factura/generar/`, {
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

export const FirmarFactura = async (id: string | undefined) => {
  try {
    await api.post(`/factura/firmar/${id}/`);
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};

export const EnviarHacienda = async (id: string) => {
  try {
    const response = await api.post(`/factura/${id}/enviar/`);
    return response;
  } catch (error) {
    console.log(error);
    throw error;
  }
};

export const getFacturaBycodigo = async (codigo_generacion: string) => {
  try {
    const response = await api.get<FacturaPorCodigoGeneracionResponse>(
      `/factura-por-codigo/`,
      {
        params: {
          codigo_generacion,
        },
      }
    );
    return response.data;
  } catch (error:any) {
    const msg = error.response.data.error
    throw new Error(msg);
  }
};

export const enviarFactura = async (id: any, formData: any) => {
  try {
    const response = await api.post(`/enviar-correo/${id}/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    console.log(response.data);
    return response.data;
  } catch (error: any) {
    console.log('ERROR:', error.response.data);
    throw new Error();
  }
};
