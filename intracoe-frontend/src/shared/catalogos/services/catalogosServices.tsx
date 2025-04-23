import axios from 'axios';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const getAllActivities = async (
  page?: number,
  limit?: number,
  filtro?: string
) => {
  try {
    const response = await axios.get(`${BASEURL}/actividad/`, {
      params: filtro ? { filtro } : {},
    });
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const getAllAmbientes = async () => {
  try {
    const response = await axios.get(`${BASEURL}/ambientes/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getAllModelosDeFacturacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/modelo-facturacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoTransmision = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-transmision/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoContingencia = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-contingencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoRentencionIVA = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-retencion-iva-mh/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTiposGeneracionDocumento = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-generacion-facturas/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTiposEstablecimientos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-establecimiento/`, {
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
    const response = await axios.get(`${BASEURL}/tipos-servicio-medico/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDTE = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-dte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllOtrosDocumentosAsociados = async () => {
  try {
    const response = await axios.get(`${BASEURL}/otros-documentos-asociado/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoIdReceptor = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-id-receptor/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllPaises = async () => {
  try {
    const response = await axios.get(`${BASEURL}/pais/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDepartamentos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/departamentos/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getDepartamentoById = async (id:number) => {
  try {
    const response = await axios.get(`${BASEURL}/departamento/${id}/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getPaisById = async (idPais: any) => {
  try {
    const response = await axios.get(`${BASEURL}/pais/${idPais}/`);
    return response.data.descripcion;
  } catch (error) {
    throw new Error();
  }
};

export const getAllMunicipios = async () => {
  try {
    const response = await axios.get(`${BASEURL}/municipio/1/`); //TODO: Modificar endpoint apra obtener todos y no por id de departamento
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllCondicioOperaciones = async () => {
  try {
    const response = await axios.get(`${BASEURL}/condicion-operacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllMetodosDePago = async () => {
  try {
    const response = await axios.get(`${BASEURL}/formas-pago/`);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const getAllPlazos = async () => {
  try {
    const response = await axios.get(`${BASEURL}/plazo/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDocContingencia = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-doc-contingencia/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoInvalidacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-invalidacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDonacion = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-donacion/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoPersona = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-persona/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoTransporte = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-transporte/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllIncoterms = async () => {
  try {
    const response = await axios.get(`${BASEURL}/incoterms/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoDomicilioFiscal = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-domicilio-fiscal/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllTipoMoneda = async () => {
  try {
    const response = await axios.get(`${BASEURL}/tipo-moneda/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const getAllDescuento = async () => {
  try {
    const response = await axios.get(`${BASEURL}/descuento/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
