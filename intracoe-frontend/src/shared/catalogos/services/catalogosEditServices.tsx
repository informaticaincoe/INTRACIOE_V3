
import { ActivitiesDataNew } from '../../interfaces/interfaces';
import { api } from '../../services/api';

export const updateActivity = async (
  id: number,
  activity: ActivitiesDataNew
) => {
  try {
    const response = await api.put(
      `/actividad/actualizar/${id}/`,
      activity,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    console.log(response);
    return response;
  } catch (error) {
    console.log(error);
  }
};

export const updateAmbientes = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/ambiente/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const updateModelosDeFacturacion = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/modelo-facturacion/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoTransmision = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-transmision/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoContingencia = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-contingencia/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoTipoRentencionIVA = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-retencion-iva-mh/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTiposGeneracionDocumento = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-generacion-documento/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTiposEstablecimientos = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipos-establecimientos/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const updateTipoServiciosMedicos = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipos-servicio-medico/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoDTE = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-dte/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateOtrosDocumentosAsociados = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/otros-documentos-asociado/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoIdReceptor = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipos-doc-id-receptor/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updatePaises = async (id: string, data: any) => {
  try {
    const response = await api.put(`/pais/${id}/editar/`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateDepartamentos = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/departamento/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateMunicipios = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/municipio/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    ); //TODO: Modificar endpoint apra obtener todos y no por id de departamento
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateCondicioOperaciones = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/condicion-operacion/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateMetodosDePago = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/formas-pago/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const updatePlazos = async (id: string, data: any) => {
  try {
    const response = await api.put(`/plazo/${id}/editar/`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoDocContingencia = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-doc-contingencia/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoInvalidacion = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-invalidacion/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoDonacion = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-donacion/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoPersona = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-persona/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoTransporte = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-transporte/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateIncoterms = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/incoterms/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoDomicilioFiscal = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-domicilio-fiscal/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateTipoMoneda = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/tipo-moneda/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const updateDescuento = async (id: string, data: any) => {
  try {
    const response = await api.put(
      `/descuento/${id}/editar/`,
      data,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
