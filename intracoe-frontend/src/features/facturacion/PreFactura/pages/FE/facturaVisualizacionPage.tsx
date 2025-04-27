import { useEffect, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router';
import { generarFacturaService } from '../../services/facturavisualizacionServices';
import { InformacionEmisor } from '../../components/shared/header/InformacionEmisor';
import {
  CuerpoDocumento,
  CuerpoDocumentoDefault,
  DatosFactura,
  DatosFacturaDefault,
  Emisor,
  EmisorDefault,
  Extension,
  ExtensionDefault,
  Receptor,
  ReceptorDefault,
  Resumen,
  resumenTablaFEDefault,
} from '../../interfaces/facturaPdfInterfaces';
import { InformacionReceptor } from '../../components/shared/receptor/InformacionReceptor';
import { TablaVentaTerceros } from '../../components/shared/ventaTerceros/tablaVentaTerceros';
import { SeccionDocumentosRelacionados } from '../../components/shared/documentosRelacionados/seccionDocumentosRelacionados';
import { SeccionOtrosDocumentosRelacionados } from '../../components/shared/otrosDocumentosRelacionados/seccionOtrosDocumentosRelacionados';
import { TablaProductosFE } from '../../components/FE/tablaProductosFE';
import { TablaResumenFE } from '../../components/FE/tablaResumenFE';
import { PagoEnLetras } from '../../components/shared/extension/pagoEnLetras';
import { CondicionOperacion } from '../../components/shared/extension/CondicionDeOperacion';
import { SeccionExtension } from '../../components/shared/extension/seccionExtension';
import { Contactos } from '../../components/shared/footer/contactos';

import { Title } from '../../../../../shared/text/title';
import { FaFilePdf } from 'react-icons/fa';
import { RiFileUploadFill } from 'react-icons/ri';
import { FaCircleCheck, FaSpinner } from 'react-icons/fa6';
import { IoMdCloseCircle } from 'react-icons/io';

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { usePDF } from 'react-to-pdf';
import { enviarFactura, EnviarHacienda, FirmarFactura } from '../../../generateDocuments/services/factura/facturaServices';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../shared/toast/customToast';
import { getCondicionDeOperacionById } from '../../../generateDocuments/services/configuracionFactura/configuracionFacturaService';

import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import { form } from 'motion/react-client';
import { Dialog } from 'primereact/dialog';

export const FacturaVisualizacionPage = () => {
  let { id } = useParams();
  const [emisor, setEmisor] = useState<Emisor>(EmisorDefault);
  const [receptor, setReceptor] = useState<Receptor>(ReceptorDefault);
  const [datosFactura, setDatosFactura] =
    useState<DatosFactura>(DatosFacturaDefault);
  const [productos, setProductos] = useState<CuerpoDocumento[]>(
    CuerpoDocumentoDefault
  );
  const [resumen, setResumen] = useState<Resumen>(resumenTablaFEDefault);
  const [extension, setExtension] = useState<Extension>(ExtensionDefault);
  const [pagoEnLetras, setPagoEnLetras] = useState<string>('');
  const [qrCode, setQrCode] = useState<string>('');
  const [condicionOperacion, setCondicionOperacion] = useState<number>(0);
  const [json, setJson] = useState<any>();
  const { targetRef } = usePDF({ filename: 'page.pdf' });
  const navigate = useNavigate();
  const toastRef = useRef<CustomToastRef>(null);

  const [loading, setLoading] = useState(false);
  const [loadingFirma, setLoadingFirma] = useState(false);

  const [viewDialog, setViewDiaog] = useState(false)

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  const generarPdf = async () => {
    const element = document.getElementById('content-id');
    if (!element) {
      throw new Error('El elemento de la factura no se encontró');
    }

    // 1) Render a canvas
    const canvas = await html2canvas(element, { useCORS: true, scale: 3 });
    const imgData = canvas.toDataURL('image/png');

    // 2) Generar el PDF en memoria
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'px' });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const ratio = canvas.height / canvas.width;
    const imgHeight = pageWidth * ratio;
    pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, imgHeight);

    // 3) Obtener el Blob del PDF
    const pdfBlob = pdf.output('blob');

    if (!pdfBlob) {
      throw new Error('No se pudo generar el PDF');
    }

    return pdfBlob;
  };



  useEffect(() => {
    firmar()
    fetchDatosFactura();
  }, []);


  const firmar = async () => {
    try {
      setLoadingFirma(true)
      const response = await FirmarFactura(id);

    } catch (error) {
      setLoadingFirma(false)
      setViewDiaog(true)
      console.log(error)
    }

  }
  const fetchCondicionOperacionDescripcion = async (id: number) => {
    const response = await getCondicionDeOperacionById(id);
    setCondicionOperacion(response.descripcion);
  };

  const enviarHacienda = async () => {
    if (id) {
      try {
        await EnviarHacienda(id);
        handleAccion(
          'success',
          <FaCircleCheck size={32} />,
          'La factura fue publicada correctamente'
        );

        // Generar PDF y JSON


        setInterval(() => navigate(0), 2000);
      } catch (error) {
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Ha ocurrido un error al publicar la factura'
        );
      }
    }
  };


  const enviarEmail = async () => {
    try {
      const pdfBlob = await generarPdf(); // Puede lanzar un error si no se genera
      if (!pdfBlob) {
        throw new Error('El archivo PDF no se pudo generar');
      }

      const jsonBlob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' });

      // Crear FormData para enviar archivos
      const formData = new FormData();
      formData.append('archivo_pdf', pdfBlob, `factura_${datosFactura.codigoGeneracion}.pdf`);
      formData.append('archivo_json', jsonBlob, `factura_${datosFactura.codigoGeneracion}.json`);

      console.log(pdfBlob)
      const emailResponse = await enviarFactura(id);
    } catch (error) {
      console.log(error)
    }
  }

  const fetchDatosFactura = async () => {
    try {
      if (id) {
        const response = await generarFacturaService(id);
        setEmisor(response.emisor);
        setDatosFactura(response.datosFactura);
        setReceptor(response.receptor);
        setProductos(response.productos);
        setResumen(response.resumen);
        setExtension(response.extension);
        setPagoEnLetras(response.pagoEnLetras);
        fetchCondicionOperacionDescripcion(response.condicionOpeacion);
        setJson(response.json);
        setQrCode(
          `https://admin.factura.gob.sv/consultaPublica?ambiente=${response.ambiente}&codGen=${response.datosFactura.codigoGeneracion.toUpperCase()}&fechaEmi=${response.datosFactura.fechaEmision}`
        );
      }
    } catch (error) {
      console.log(error);
    }
  };

  // … dentro de tu componente FacturaVisualizacionPage:

  const downloadZip = async () => {
    setLoading(true);

    const element = document.getElementById('content-id');
    if (!element) return;

    // 1) Render a canvas
    const canvas = await html2canvas(element, { useCORS: true, scale: 3 });
    const imgData = canvas.toDataURL('image/png');

    // 2) Genera el PDF en memoria
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'px' });
    const pageWidth = pdf.internal.pageSize.getWidth();
    const ratio = canvas.height / canvas.width;
    const imgHeight = pageWidth * ratio;
    pdf.addImage(imgData, 'PNG', 0, 0, pageWidth, imgHeight);

    // 3) Obtén el Blob del PDF
    const pdfBlob = pdf.output('blob');

    // 4) Crea el Blob del JSON
    //    Asume que lo tienes en el estado `json`
    const jsonString = JSON.stringify(json, null, 2);
    const jsonBlob = new Blob([jsonString], { type: 'application/json' });

    // 5) Empaqueta todo en un ZIP
    const zip = new JSZip();
    zip.file(`factura_${datosFactura.codigoGeneracion}.pdf`, pdfBlob);
    zip.file(`factura_${datosFactura.codigoGeneracion}.json`, jsonBlob);
    console.log(pdfBlob);
    console.log(jsonBlob);


    // 6) Genera el ZIP y dispara la descarga
    const zipBlob = await zip.generateAsync({ type: 'blob' });
    saveAs(zipBlob, `factura_${datosFactura.codigoGeneracion}.zip`);
    setLoading(false);
  };

  return (
    <>
      <Title text="Factura generada con éxito" />

      <div className="flex justify-center gap-5">
        <button
          onClick={downloadZip}
          className="mt-5 mb-7 rounded-md bg-red-700 px-8 py-3 text-white"
        >
          <span className="flex items-center justify-center gap-2">
            {loading ? (
              <span className="flex items-center gap-2">
                <FaSpinner className="animate-spin text-white" />
                Convirtiendo...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                <FaFilePdf size={24} className="text-white" />
                <p>Descargar Factura</p>
              </span>
            )}
          </span>
        </button>
        {datosFactura.selloRemision == null && (
          <button
            onClick={enviarHacienda}
            className="bg-primary-blue mt-5 mb-7 rounded-md px-8 py-3 text-white"
          >
            <span className="flex items-center justify-center gap-2">
              <RiFileUploadFill size={24} />
              <p>Publicar</p>
            </span>
          </button>
        )}
        <button
          onClick={() => navigate('/generar-documentos')}
          className="border-primary-blue text-primary-blue mt-5 mb-7 rounded-md border bg-white px-8 py-3"
        >
          Realizar otra factura
        </button>
        <button onClick={enviarEmail}>ENviar email</button>
      </div>
      <div
        id="content-id"
        style={{
          fontSize: '1vw',
          padding: '0.7vw 2vw',
        }}
      >
        <div
          className="my-2 flex flex-col gap-5 bg-white px-10 py-8"
          ref={targetRef}
        >
          <InformacionEmisor
            qrCode={qrCode}
            emisor={emisor}
            datosFactura={datosFactura}
          />
          <InformacionReceptor receptor={receptor} />
          <TablaVentaTerceros />
          <SeccionDocumentosRelacionados />
          {datosFactura.tipoDte != '05' && (
            <SeccionOtrosDocumentosRelacionados />
          )}
          <div className="flex flex-col">
            <TablaProductosFE
              productos={productos}
              tipo_dte={datosFactura.tipoDte}
            />
            <div id="footer">
              <div className="grid grid-cols-2 gap-x-5 pt-5">
                <span className="flex flex-col gap-3">
                  <PagoEnLetras cantidadAPagar={pagoEnLetras} />
                  <CondicionOperacion condicion={condicionOperacion} />
                  <div className="border-border-color rounded-md border-2 px-4 py-3 text-start">
                    <div className="flex">
                      <p>
                        <span className="font-bold">Oberservaciones: </span>
                        {extension.observaciones}
                      </p>
                      <p>
                        <span className="font-bold"></span>
                        {extension.nombEntrega}
                      </p>
                    </div>
                  </div>
                  <SeccionExtension extension={extension} />
                </span>
                <span>
                  <TablaResumenFE resumen={resumen} />
                </span>
              </div>
              <Contactos emisor={emisor} />
            </div>
          </div>
        </div>
      </div>
      <CustomToast ref={toastRef} />
      {
        viewDialog &&
        <Dialog header="Error en firma de dte" visible={viewDialog} style={{ width: '50vw' }} onHide={() => { if (!viewDialog) return; setViewDiaog(false); }}>
          <div className='flex flex-col justify-center w-full items-center'>
            <p className="m-0">
              ¿Desea intentar de nuevo?
            </p>
            <span className='flex w-full items-center justify-center gap-4 pt-5'>
            <button onClick={firmar} className='flex bg-primary-blue text-white px-7 py-3 rounded'>{loadingFirma ? 'cargando...' : 'reintentar'}</button>
            <button onClick={()=> setViewDiaog(false)} className='flex border border-primary-blue text-primary-blue px-7 py-3 rounded'>Cancelar</button>
              </span>
          </div>
        </Dialog>
      }
    </>
  );
};
