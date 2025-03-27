import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { EnviarHacienda, FirmarFactura, generarFacturaService } from "../../services/facturavisualizacionServices";
import { InformacionEmisor } from "../../components/shared/header/InformacionEmisor";
import { CuerpoDocumento, CuerpoDocumentoDefault, DatosFactura, DatosFacturaDefault, Emisor, EmisorDefault, Extension, ExtensionDefault, Receptor, ReceptorDefault, ResumenDefalt, resumenTablaFE, resumenTablaFEDefault } from "../../interfaces/facturaPdfInterfaces";
import { InformacionReceptor } from "../../components/shared/receptor/InformacionReceptor";
import { TablaVentaTerceros } from "../../components/shared/ventaTerceros/tablaVentaTerceros";
import { SeccionDocumentosRelacionados } from "../../components/shared/documentosRelacionados/seccionDocumentosRelacionados";
import { SeccionOtrosDocumentosRelacionados } from "../../components/shared/otrosDocumentosRelacionados/seccionOtrosDocumentosRelacionados";
import { TablaProductosFE } from "../../components/FE/tablaProductosFE";
import { TablaResumenFE } from "../../components/FE/tablaResumenFE";
import { PagoEnLetras } from "../../components/shared/extension/pagoEnLetras";
import { CondicionOperacion } from "../../components/shared/extension/CondicionDeOperacion";
import { SeccionExtension } from "../../components/shared/extension/seccionExtension";
import { Contactos } from "../../components/shared/footer/contactos";

import { Title } from "../../../../../shared/text/title";

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { usePDF } from "react-to-pdf";


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
    const x = (pageWidth - imgWidth) / 2; // normalmente esto será 0, pero lo dejamos flexible

    // ✅ Añadir imagen con altura real proporcional

    pdf.addImage(imgData, 'PNG', xOffset, 0, imgWidth, imgHeight);
    pdf.save('factura.pdf');
};



export const FacturaVisualizacionPage = () => {
    let { id } = useParams();
    const [emisor, setEmisor] = useState<Emisor>(EmisorDefault)
    const [receptor, setReceptor] = useState<Receptor>(ReceptorDefault)
    const [datosFactura, setDatosFactura] = useState<DatosFactura>(DatosFacturaDefault)
    const [productos, setProductos] = useState<CuerpoDocumento[]>(CuerpoDocumentoDefault)
    const [resumen, setResumen] = useState<resumenTablaFE>(resumenTablaFEDefault)
    const [extension, setExtension] = useState<Extension>(ExtensionDefault)
    const [pagoEnLetras, setPagoEnLetras] = useState<string>("")
    const [condicionOperacion, setCondicionOperacion] = useState<number>(0)

    const { toPDF, targetRef } = usePDF({ filename: 'page.pdf' });
    useEffect(() => {
        fetchDatosFactura()
    }, [])

    const fetchDatosFactura = async () => {
        try {
            if (id) {
                const response = await generarFacturaService(id)
                console.log(response.emisor)
                console.log(response.receptor)
                setEmisor(response.emisor)
                setDatosFactura(response.datosFactura)
                setReceptor(response.receptor)
                setProductos(response.productos)
                setResumen(response.resumen)
                setExtension(response.extension)
                setPagoEnLetras(response.pagoEnLetras)
                setCondicionOperacion(response.condicionOpeacion)
            }
        }
        catch (error) {
            console.log(error)
        }
    }

    const firmarFactura = async () => {
        try {
            if (id) {
                const response = await FirmarFactura(id)
                console.log(response)
                enviarHacienda()
            }
        } catch (error) {
            console.log(error)
        }
    }

    const enviarHacienda = async () => {
        if (id) {
            try {
                const response = await EnviarHacienda(id)
            } catch (error) {
                console.log(error)
            }
        }
    }
    return (
        <>
            <Title text="Factura" />

            <button onClick={exportToPDF}>
                Descargar PDF
            </button>

            <button onClick={firmarFactura}>
                Enviar Hacienda
            </button>

            <div>
                <button onClick={() => toPDF()}>Download PDF</button>
            </div>
            <div id="content-id"
                style={{
                    background: '#fff',
                    fontSize: '1vw',
                    padding: '2vw',

                }}>
                <div className="py-5 px-2 my-2 bg-white" ref={targetRef}>
                    <InformacionEmisor emisor={emisor} datosFactura={datosFactura} />
                    <InformacionReceptor receptor={receptor} />
                    <TablaVentaTerceros />
                    <SeccionDocumentosRelacionados />
                    <SeccionOtrosDocumentosRelacionados />
                    <TablaProductosFE productos={productos} />
                    <div className="grid grid-cols-2 pt-5 gap-x-5">
                        <span className="flex flex-col gap-3">
                            <PagoEnLetras cantidadAPagar={pagoEnLetras} />
                            <CondicionOperacion condicion={condicionOperacion} />
                            <div className="border-2 border-border-color rounded-md text-start py-3 px-4">
                                <div className="flex ">
                                    <p><span className="font-bold">Oberservaciones: </span>{extension.observaciones}</p>
                                    <p><span className="font-bold"></span>{extension.nombEntrega}</p>
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
        </>
    )
}