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
import { FaCircleCheck } from 'react-icons/fa6';
import { IoMdCloseCircle } from 'react-icons/io';

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { usePDF } from 'react-to-pdf';
import { EnviarHacienda } from '../../../generateDocuments/services/factura/facturaServices';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../shared/toast/customToast';
import { getCondicionDeOperacionById } from '../../../generateDocuments/services/configuracionFactura/configuracionFacturaService';

const exportToPDF = async () => {
  const element = document.getElementById('content-id');
  if (!element) return;

  const canvas = await html2canvas(element, {
    useCORS: true,
    scale: 3, // mejor resolución
  });

  const imgData = canvas.toDataURL('image/png');

  const pdf = new jsPDF({
    orientation: 'portrait',
    unit: 'px',
  });

  const pageWidth = pdf.internal.pageSize.getWidth();

  // 🧠 Calcular altura proporcional manteniendo aspecto
  const imgProps = {
    width: canvas.width,
    height: canvas.height,
  };

  const ratio = imgProps.height / imgProps.width;
  const imgHeight = pageWidth * ratio;
  const xOffset = (pageWidth - canvas.width * (pageWidth / canvas.width)) / 2;
  const imgWidth = pageWidth;

  // ✅ Añadir imagen con altura real proporcional
  pdf.addImage(imgData, 'PNG', xOffset, 0, imgWidth, imgHeight);
  pdf.save('factura.pdf');
};

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
  const [condicionOperacion, setCondicionOperacion] = useState<number>(0);
  const navigate = useNavigate();
  const { targetRef } = usePDF({ filename: 'page.pdf' });
  const toastRef = useRef<CustomToastRef>(null);
  const [qrCode, setQrCode] = useState<string>('');

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

  useEffect(() => {
    fetchDatosFactura();
  }, []);

  const fetchCondicionOperacionDescripcion = async (id: number) => {
    const response = await getCondicionDeOperacionById(id);
    setCondicionOperacion(response.descripcion);
  };

  const enviarHacienda = async () => {
    if (id) {
      try {
        const response = await EnviarHacienda(id);
        handleAccion(
          'success',
          <FaCircleCheck size={32} />,
          'La factura fue publicada correctamente'
        );
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
        setQrCode(
          `https://admin.factura.gob.sv/consultaPublica?ambiente=${response.ambiente}&codGen=${response.datosFactura.codigoGeneracion.toUpperCase()}&fechaEmi=${response.datosFactura.fechaEmision}`
        );
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <Title text="Factura generada con éxito" />

      <div className="flex justify-center gap-5">
        <button
          onClick={exportToPDF}
          className="mt-5 mb-7 rounded-md bg-red-700 px-8 py-3 text-white"
        >
          <span className="flex items-center justify-center gap-2">
            <FaFilePdf size={24} />
            <p>Descargar PDF</p>
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
    </>
  );
};
