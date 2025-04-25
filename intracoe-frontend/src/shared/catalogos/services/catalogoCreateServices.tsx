import { api } from '../../services/api';

export const createActivities = async (body: any) => {
  try {
    const response = await api.post(`/actividad/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const createAmbientes = async (body: any) => {
  try {
    const response = await api.post(`/ambiente/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const createModelosDeFacturacion = async (body: any) => {
  try {
    const response = await api.post(`/modelo-facturacion/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoTransmision = async (body: any) => {
  try {
    const response = await api.post(`/tipo-transmision/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoContingencia = async (body: any) => {
  try {
    const response = await api.post(`/tipo-contingencia/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoRentencionIVA = async (body: any) => {
  try {
    const response = await api.post(`/tipo-retencion-iva-mh/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTiposGeneracionDocumento = async (body: any) => {
  try {
    const response = await api.post(`/tipo-generacion-documento/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTiposEstablecimientos = async (body: any) => {
  try {
    const response = await api.post(`/tipos-establecimientos/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const createTipoServiciosMedicos = async (body: any) => {
  try {
    const response = await api.post(`/tipos-servicio-medico/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDTE = async (body: any) => {
  try {
    const response = await api.post(`/tipo-dte/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createOtrosDocumentosAsociados = async (body: any) => {
  try {
    const response = await api.post(`/otros-documentos-asociado/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoIdReceptor = async (body: any) => {
  try {
    const response = await api.post(`/tipos-doc-id-receptor/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createPaises = async (body: any) => {
  try {
    const response = await api.post(`/pais/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createDepartamentos = async (body: any) => {
  try {
    const response = await api.post(`/departamento/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createPaisById = async (body: any) => {
  try {
    const response = await api.post(`/pais/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data.descripcion;
  } catch (error) {
    throw new Error();
  }
};

export const createMunicipios = async (body: any) => {
  try {
    const response = await api.post(`/municipio/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createCondicioOperaciones = async (body: any) => {
  try {
    const response = await api.post(`/condicion-operacion/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createMetodosDePago = async (body: any) => {
  try {
    const response = await api.post(`/formas-pago/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const createPlazos = async (body: any) => {
  try {
    const response = await api.post(`/plazo/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDocContingencia = async (body: any) => {
  try {
    const response = await api.post(`/tipo-doc-contingencia/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoInvalidacion = async (body: any) => {
  try {
    const response = await api.post(`/tipo-invalidacion/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDonacion = async (body: any) => {
  try {
    const response = await api.post(`/tipo-donacion/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoPersona = async (body: any) => {
  try {
    const response = await api.post(`/tipo-persona/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoTransporte = async (body: any) => {
  try {
    const response = await api.post(`/tipo-transporte/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createIncoterms = async (body: any) => {
  try {
    const response = await api.post(`/incoterms/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDomicilioFiscal = async (body: any) => {
  try {
    const response = await api.post(`/tipo-domicilio-fiscal/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoMoneda = async (body: any) => {
  try {
    const response = await api.post(`/tipo-moneda/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createDescuento = async (body: any) => {
  try {
    const response = await api.post(`/descuento/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
