import axios from 'axios';
import { FacturaResponse } from '../interfaces/facturaPdfInterfaces';

const BASEURL = import.meta.env.VITE_URL_BASE;

export const generarFacturaService = async (id: string) => {
  try {
    const response = await axios.get<FacturaResponse>(
      `${BASEURL}/factura_pdf/${id}/`
    );
    return {
      emisor: response.data.json_original.emisor,
      receptor: response.data.json_original.receptor,
      datosFactura: {
        tipoDte: response.data.json_original.identificacion.tipoDte,
        codigoGeneracion: response.data.codigo_generacion,
        numeroControl: response.data.numero_control,
        fechaEmision: response.data.fecha_emision,
        horaEmision: response.data.hora_emision,
        selloRemision: response.data.sello_recepcion,
      },
      productos: response.data.json_original.cuerpoDocumento,
      resumen: {
        totalNoSuj: response.data.total_no_sujetas,
        totalExenta: response.data.total_exentas,
        totalGravada: response.data.total_gravadas,
        subTotalVentas: response.data.sub_total_ventas,
        descuNoSuj: response.data.total_no_sujetas,
        descuExenta: response.data.descuento_exento,
        descuGravada: response.data.descuento_gravado,
        porcentajeDescuento: response.data.por_descuento,
        totalDescu: response.data.total_descuento,
        subTotal: response.data.sub_total,
        ivaRete: response.data.iva_retenido,
        reteRenta: response.data.retencion_renta,
        montoTotalOperacion: response.data.total_operaciones,
        totalNoGravado: response.data.total_no_gravado,
        totalPagar: response.data.total_pagar,
        totalIva: response.data.total_iva,
        saldoFavor: response.data.saldo_favor,
        condicionOperacion: response.data.condicion_operacion,
        pagos: response.data.formas_Pago,
        numPagoElectronico:
          response.data.json_original.resumen.numPagoElectronico,
        tributos: response.data.json_original.resumen.tributos,
        totalLetras: response.data.total_letras,
      },
      pagoEnLetras: response.data.total_letras,
      condicionOpeacion: response.data.condicion_operacion,
      extension: response.data.json_original.extension,
      ambiente: response.data.json_original.identificacion.ambiente,
    };
  } catch (error) {
    console.log(error);
    throw new Error();
  }
};
