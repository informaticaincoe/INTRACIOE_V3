import { ActivitiesInterfacePagination, OtrosDocumentosAsociados, OtrosDocumentosAsociadosResponse } from '../../interfaces/interfaces';
import { api } from '../../services/api';

export const getAllActivities = async (
  page?: number,
  limit?: number,
  filtro?: string
) => {
  try {
    const response = await api.get(`/actividad/`, {
      params: filtro ? { filtro } : {},
    });
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const getAllAmbientes = async () => {
  try {
    const response = await api.get(`/ambientes/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getAllActivitiesPagination = async (
  page?: number,
  limit?: number,
  filtro?: string
) => {
  const queryParams = new URLSearchParams();

  //paginacion
  queryParams.append('page', String(page));
  queryParams.append('page_size', String(limit));

  try {
    const response = await api.get<ActivitiesInterfacePagination>(
      `/actividad/`,
      {
        params: { page: page, page_size: limit, filtro: filtro },
      }
    );

    return {
      results: response.data.results,
      current_page: response.data.current_page,
      page_size: response.data.page_size,
      has_next: response.data.has_next,
      has_previous: response.data.has_previous,
      count: response.data.count,
    };
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const getAllModelosDeFacturacion = async () => {
  try {
    const response = await api.get(`/modelo-facturacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoTransmision = async () => {
  try {
    const response = await api.get(`/tipo-transmision/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoContingencia = async () => {
  try {
    const response = await api.get(`/tipo-contingencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoRentencionIVA = async () => {
  try {
    const response = await api.get(`/tipo-retencion-iva-mh/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTiposGeneracionDocumento = async () => {
  try {
    const response = await api.get(`/tipo-generacion-facturas/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTiposEstablecimientos = async () => {
  try {
    const response = await api.get(`/tipo-establecimiento/`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getAllTipoServiciosMedicos = async () => {
  try {
    const response = await api.get(`/tipos-servicio-medico/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDTE = async () => {
  try {
    const response = await api.get(`/tipo-dte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllOtrosDocumentosAsociados = async () => {
  try {
    const response = await api.get(`/otros-documentos-asociado/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getOtrosDocumentosAsociadosById = async (id: string) => {
  try {
    const response = await api.get<OtrosDocumentosAsociadosResponse>(`/otros-documentos-asociado/${id}/`);
    console.log(response.data)
    return response.data;
    
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoIdReceptor = async () => {
  try {
    const response = await api.get(`/tipo-id-receptor/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllPaises = async () => {
  try {
    const response = await api.get(`/pais/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDepartamentos = async () => {
  try {
    const response = await api.get(`/departamentos/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getDepartamentoById = async (id: number) => {
  try {
    const response = await api.get(`/departamento/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getPaisById = async (idPais: any) => {
  try {
    const response = await api.get(`/pais/${idPais}/`);
    return response.data.descripcion;
  } catch (error) {
    throw new Error();
  }
};

export const getAllMunicipios = async () => {
  try {
    const response = await api.get(`/municipio/1/`); //TODO: Modificar endpoint apra obtener todos y no por id de departamento
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllCondicioOperaciones = async () => {
  try {
    const response = await api.get(`/condicion-operacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllMetodosDePago = async () => {
  try {
    const response = await api.get(`/formas-pago/`);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getAllPlazos = async () => {
  try {
    const response = await api.get(`/plazo/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDocContingencia = async () => {
  try {
    const response = await api.get(`/tipo-doc-contingencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoInvalidacion = async () => {
  try {
    const response = await api.get(`/tipo-invalidacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDonacion = async () => {
  try {
    const response = await api.get(`/tipo-donacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoPersona = async () => {
  try {
    const response = await api.get(`/tipo-persona/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoTransporte = async () => {
  try {
    const response = await api.get(`/tipo-transporte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllIncoterms = async () => {
  try {
    const response = await api.get(`/incoterms/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDomicilioFiscal = async () => {
  try {
    const response = await api.get(`/tipo-domicilio-fiscal/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllRegimenFiscal = async () => {
  try {
    const response = await api.get(`/regimen-fiscal/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllRecintoFiscal = async () => {
  try {
    const response = await api.get(`/recinto-fiscal/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoMoneda = async () => {
  try {
    const response = await api.get(`/tipo-moneda/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDescuento = async () => {
  try {
    const response = await api.get(`/descuento/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllSecuencias = async () => {
  try {
    const response = await api.get(`/secuencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};