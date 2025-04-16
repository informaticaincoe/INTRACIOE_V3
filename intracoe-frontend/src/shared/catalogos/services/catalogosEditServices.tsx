import axios from 'axios';
import { ActivitiesDataNew } from '../../interfaces/interfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const updateActivity = async (
  id: number,
  activity: ActivitiesDataNew
) => {
  try {
    const response = await axios.put(
      `${BASEURL}/actividad/actualizar/${id}/`,
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
    const response = await axios.put(
      `${BASEURL}/ambiente/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/modelo-facturacion/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-transmision/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-contingencia/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-retencion-iva-mh/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-generacion-documento/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipos-establecimientos/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipos-servicio-medico/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-dte/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/otros-documentos-asociado/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipos-doc-id-receptor/${id}/editar/`,
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
    const response = await axios.put(`${BASEURL}/pais/${id}/editar/`, data, {
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
    const response = await axios.put(
      `${BASEURL}/departamento/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/municipio/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/condicion-operacion/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/formas-pago/${id}/editar/`,
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
    const response = await axios.put(`${BASEURL}/plazo/${id}/editar/`, data, {
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
    const response = await axios.put(
      `${BASEURL}/tipo-doc-contingencia/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-invalidacion/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-donacion/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-persona/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-transporte/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/incoterms/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-domicilio-fiscal/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/tipo-moneda/${id}/editar/`,
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
    const response = await axios.put(
      `${BASEURL}/descuento/${id}/editar/`,
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
