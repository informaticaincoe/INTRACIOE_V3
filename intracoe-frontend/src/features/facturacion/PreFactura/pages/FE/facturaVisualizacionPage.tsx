import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import { generarFacturaService } from "../../services/facturavisualizacionServices";
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
    return (
        <div className="flex justify-between items-center w-full">
            <div className="py-5 px-5 w-3/5 bg-white border">
                <InformacionEmisor emisor={emisor} datosFactura={datosFactura} />
                <InformacionReceptor receptor={receptor} />
                <TablaVentaTerceros />
                <SeccionDocumentosRelacionados />
                <SeccionOtrosDocumentosRelacionados />
                <TablaProductosFE productos={productos} />
                <div className="grid grid-cols-2 py-5 gap-x-5">
                    <span className="flex flex-col gap-7">
                        <PagoEnLetras cantidadAPagar={pagoEnLetras} />
                        <CondicionOperacion condicion={condicionOperacion} />
                        <SeccionExtension extension={extension} />
                    </span>
                    <span>
                        <TablaResumenFE resumen={resumen} />
                    </span>
                </div>
                <Contactos emisor={emisor} />
            </div>
        </div>
    )
}