import { api } from '../../services/api';

export const deleteActivities = async (
  page?: number,
  limit?: number,
  filtro?: string
) => {
  try {
    const response = await api.delete(`/actividad/eliminar/`, {
      params: filtro ? { filtro } : {},
    });
    return response.data;
  } catch (error) {
    console.log('Error en la solicitud:', error);
  }
};

export const deleteAmbientes = async (id: number) => {
  try {
    const response = await api.delete(`/ambiente/${id}/eliminar/`, {
      headers: {
        'Content-Type': 'application/json', // Asegúrate de que se está enviando como JSON
      },
    });

    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const deleteModelosDeFacturacion = async (id: number) => {
  try {
    const response = await api.delete(`/modelo-facturacion/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoTransmision = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-transmision/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoContingencia = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-contingencia/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoRentencionIVA = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-retencion-iva-mh/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTiposGeneracionDocumento = async (id: number) => {
  try {
    const response = await api.delete(
      `/tipo-generacion-documento/${id}/eliminar/`
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTiposEstablecimientos = async (id: number) => {
  try {
    const response = await api.delete(
      `/tipos-establecimientos/${id}/eliminar/`,
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

export const deleteTipoServiciosMedicos = async (id: number) => {
  try {
    const response = await api.delete(`/tipos-servicio-medico/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoDTE = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-dte/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteOtrosDocumentosAsociados = async (id: number) => {
  try {
    const response = await api.delete(
      `/otros-documentos-asociado/${id}/eliminar/`
    );
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoIdReceptor = async (id: number) => {
  try {
    const response = await api.delete(`/tipos-doc-id-receptor/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deletePaises = async (id: number) => {
  try {
    const response = await api.delete(`/pais/${id}/eliminar/`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteDepartamentos = async (id: number) => {
  try {
    const response = await api.delete(`/departamento/${id}/eliminar/`);

    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deletePaisById = async (idPais: any) => {
  try {
    const response = await api.delete(`/pais/${idPais}/eliminar/`);
    return response.data.descripcion;
  } catch (error) {
    throw new Error();
  }
};

export const deleteMunicipios = async (id: number) => {
  try {
    const response = await api.delete(`/municipio/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteCondicioOperaciones = async (id: number) => {
  try {
    const response = await api.delete(`/condicion-operacion/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteMetodosDePago = async (id: number) => {
  try {
    const response = await api.delete(`/formas-pago/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    console.log(error);
  }
};

export const deletePlazos = async (id: number) => {
  try {
    const response = await api.delete(`/plazo/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoDocContingencia = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-doc-contingencia/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoInvalidacion = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-invalidacion/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoDonacion = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-donacion/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoPersona = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-persona/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoTransporte = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-transporte/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteIncoterms = async (id: number) => {
  try {
    const response = await api.delete(`/incoterms/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoDomicilioFiscal = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-domicilio-fiscal/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteTipoMoneda = async (id: number) => {
  try {
    const response = await api.delete(`/tipo-moneda/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteDescuento = async (id: number) => {
  try {
    const response = await api.delete(`/descuento/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};

export const deleteSecuencia = async (id: number) => {
  try {
    const response = await api.delete(`/secuencia/${id}/eliminar/`);
    return response.data;
  } catch (error) {
    throw new Error();
  }
};
