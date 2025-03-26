import axios from 'axios';
import { FacturaResponse } from '../interfaces/facturaPdfInterfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (id: string) => {
  try {
    const response = await axios.get<FacturaResponse>(`${BASEURL}/factura_pdf/${id}/`);
    console.log("response.data", response.data)
    return {
      emisor: response.data.json_original.emisor,
      receptor: response.data.json_original.receptor,
      datosFactura: {
        codigoGeneracion: response.data.codigo_generacion,
        numeroControl:response.data.numero_control,
        fechaEmision: response.data.fecha_emision,
        horaEmision: response.data.hora_emision
      },
    };
  } catch (error) {
    console.log(error)
    throw new Error();
  }
};