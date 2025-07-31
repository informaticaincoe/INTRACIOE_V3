import { api } from "../../../../../shared/services/api";

export const getFacturaCodigosSujetoExcluido = async () => {
  try {
    const response = await api.get(`/factura/generar_sujeto_excluido/`);

    console.log("DATA TIPO 14", response.data)

    return response.data

  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
