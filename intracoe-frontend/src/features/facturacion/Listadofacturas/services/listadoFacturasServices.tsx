import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

interface FacturaParams {
  page?: number;
  limit?: number;
  recibido_mh?: string;
  sello_recepcion?: string;
  has_sello_recepcion?: 'yes' | 'no';
  tipo_dte?: string;
}

export const getAllFacturas = async (params: FacturaParams = {}) => {
  try {
    const response = await axios.get(`${BASEURL}/facturas/`, {
      params: {
        page: params.page ?? 1,
        limit: params.limit ?? 20,
        recibido_mh: params.recibido_mh,
        sello_recepcion: params.sello_recepcion,
        has_sello_recepcion: params.has_sello_recepcion,
        tipo_dte: params.tipo_dte,
      }
    });

    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
    throw error;
  }
};