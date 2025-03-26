import axios from 'axios';
import { FacturaResponse } from '../interfaces/facturaPdfInterfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (id: string) => {
  try {
    const response = await axios.get(`${BASEURL}/factura_pdf/${id}/`);
    console.log("response.data", response.data)
    return {
      emisor: response.data.json_original.emisor,
      receptor: response.data.json_original.receptor,
      datosFactura: {
        codigoGeneracion: response.data.codigo_generacion,
        numeroControl: response.data.numero_control,
        fechaEmision: response.data.fecha_emision,
        horaEmision: response.data.hora_emision
      },
      productos: response.data.json_original.cuerpoDocumento,
      resumen: {
        totalExenta: response.data.total_exentas,
        totalGravada: response.data.total_gravadas,
        subTotalVentas: response.data.sub_total_ventas,
        descuNoSuj: response.data.total_no_sujetas,
        descuExenta: response.data.descuento_exento,
        descuGravada: response.data.descuento_gravado,
        // porcentajeDescuento: response.data.,
        // totalDescu: response.data.,
        subTotal: response.data.sub_total,
        ivaRete: response.data.iva_retenido,
        reteRenta: response.data.retencion_renta,
        montoTotalOperacion: response.data.total_operaciones,
        totalNoGravado: response.data.total_no_gravado,
        totalPagar: response.data.total_pagar,
        totalIva: response.data.total_iva
      },
      pagoEnLetras: response.data.total_letras,
      condicionOpeacion: response.data.condicion_operacion,
      extension: response.data.json_original.extension
    };
  } catch (error) {
    console.log(error)
    throw new Error();
  }
};

export const FirmarFactura = async (id: string) => {
  try {
    const response = await axios.post(`${BASEURL}/factura/firmar/${id}/`);
    console.log(response)
  }
  catch (error) {
    console.log(error)
  }
}

export const EnviarHacienda = async(id:string) =>{
  try {
    const response = await axios.post(`${BASEURL}/factura/enviar_hacienda/${id}/`);
    console.log(response)
  } catch (error) {
    console.log(error)
  }
}