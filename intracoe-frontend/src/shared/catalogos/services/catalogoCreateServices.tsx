import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const createActivities = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/actividad/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/ambiente/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/modelo-facturacion/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoTransmision = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipo-transmision/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoContingencia = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipo-contingencia/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoRentencionIVA = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipo-retencion-iva-mh/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTiposGeneracionDocumento = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipo-generacion-documento/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTiposEstablecimientos = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipos-establecimientos/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const createTipoServiciosMedicos = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipos-servicio-medico/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDTE = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/tipo-dte/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/otros-documentos-asociado/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoIdReceptor = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipos-doc-id-receptor/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createPaises = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/pais/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/departamento/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/pais/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/municipio/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/condicion-operacion/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createMetodosDePago = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/formas-pago/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/plazo/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/tipo-doc-contingencia/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoInvalidacion = async (body: any) => {
  try {
    const response = await axios.post(
      `${BASEURL}/tipo-invalidacion/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoDonacion = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/tipo-donacion/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/tipo-persona/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/tipo-transporte/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createIncoterms = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/incoterms/crear/`, body, {
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
    const response = await axios.post(
      `${BASEURL}/tipo-domicilio-fiscal/crear/`,
      body,
      {
        headers: {
          'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
        },
      }
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const createTipoMoneda = async (body: any) => {
  try {
    const response = await axios.post(`${BASEURL}/tipo-moneda/crear/`, body, {
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
    const response = await axios.post(`${BASEURL}/descuento/crear/`, body, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
