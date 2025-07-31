import { FiltersListadoFacturas } from '../../../../shared/interfaces/interfaceFacturaJSON';
import { api } from '../../../../shared/services/api';

export interface FacturaParams {
  page?: number;
  limit?: number;
  filters?: FiltersListadoFacturas;
}

export const getAllFacturas = async (
  { page, limit, filters }: FacturaParams = {
    page: 1,
    limit: 100,
    filters: undefined,
  }
) => {
  try {
    const queryParams = new URLSearchParams();

    //paginacion
    queryParams.append('page', String(page));
    queryParams.append('page_size', String(limit));

    // Agregar filtros si existen
    if (filters?.recibido_mh !== null) {
      queryParams.append('recibido_mh', String(filters?.recibido_mh));
    }
    if (filters?.sello_recepcion) {
      queryParams.append('sello_recepcion', filters?.sello_recepcion);
    }
    if (filters?.has_sello_recepcion !== null) {
      queryParams.append(
        'has_sello_recepcion',
        String(filters?.has_sello_recepcion)
      );
    }
    if (filters?.estado !== null) {
      queryParams.append('estado', String(filters?.estado));
    }
    if (filters?.estado_invalidacion !== null) {
      queryParams.append(
        'estado_invalidacion',
        String(filters?.estado_invalidacion)
      );
    }
    if (filters?.tipo_dte) {
      queryParams.append('tipo_dte', filters?.tipo_dte);
    }

    if (!filters) {
      queryParams.append('all', 'true');
    }

    const response = await api.get(`/facturas/?${queryParams.toString()}`);

    return (
      response.data || {
        results: [],
        current_page: 1,
        page_size: limit,
        total_pages: 1,
        total_records: 0,
      }
    );
  } catch (error) {
    console.log('Error en la solicitud:', error);
    throw error;
  }
};

export const getAllFacturasSujetoExcluido = async (
  { page, limit, filters }: FacturaParams = {
    page: 1,
    limit: 100,
    filters: undefined,
  }
) => {
  try {
    const queryParams = new URLSearchParams();

    //paginacion
    queryParams.append('page', String(page));
    queryParams.append('page_size', String(limit));

    // Agregar filtros si existen
    if (filters?.recibido_mh !== null) {
      queryParams.append('recibido_mh', String(filters?.recibido_mh));
    }
    if (filters?.sello_recepcion) {
      queryParams.append('sello_recepcion', filters?.sello_recepcion);
    }
    if (filters?.has_sello_recepcion !== null) {
      queryParams.append(
        'has_sello_recepcion',
        String(filters?.has_sello_recepcion)
      );
    }
    if (filters?.estado !== null) {
      queryParams.append('estado', String(filters?.estado));
    }
    if (filters?.estado_invalidacion !== null) {
      queryParams.append(
        'estado_invalidacion',
        String(filters?.estado_invalidacion)
      );
    }
    if (filters?.tipo_dte) {
      queryParams.append('tipo_dte', filters?.tipo_dte);
    }

    if (!filters) {
      queryParams.append('all', 'true');
    }

    const response = await api.get(`/facturas-sujeto-excluido/?${queryParams.toString()}`);
    console.log("response", response)
    return (
      response.data || {
        results: [],
        current_page: 1,
        page_size: limit,
        total_pages: 1,
        total_records: 0,
      }
    );
  } catch (error) {
    console.log('Error en la solicitud:', error);
    throw error;
  }
};

export const invalidarDte = async (factura_id: number) => {
  try {
    const response = await api.post(`/invalidar_dte/${factura_id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const invalidarDteSujetoExcluido = async (factura_id: number) => {
  try {
    const response = await api.post(`/invalidar_dte_sujeto_excluido/${factura_id}/`);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};
