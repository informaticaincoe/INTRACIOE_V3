import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { generarFacturaService } from "../../services/facturavisualizacionServices";
import { InformacionEmisor } from "../../components/shared/header/InformacionEmisor";
import { DatosFactura, DatosFacturaDefault, Emisor, EmisorDefault, Receptor, ReceptorDefault } from "../../interfaces/facturaPdfInterfaces";
import { InformacionReceptor } from "../../components/shared/receptor/InformacionReceptor";
import { TablaVentaTerceros } from "../../components/shared/ventaTerceros/tablaVentaTerceros";

export const FacturaVisualizacionPage = () => {
    let { id } = useParams();
    const [emisor, setEmisor] = useState<Emisor>(EmisorDefault)
    const [receptor, setReceptor] = useState<Receptor>(ReceptorDefault)

    const [datosFactura, setDatosFactura] = useState<DatosFactura>(DatosFacturaDefault)

    useEffect(() => {
        fetchDatosFactura()
    },[])

    const fetchDatosFactura = async () => {
        try {
            if(id) {
                const response = await  generarFacturaService(id)
                console.log(response.emisor)
                console.log(response.receptor)
                setEmisor(response.emisor)
                setDatosFactura(response.datosFactura)
                setReceptor(response.receptor)
            }
        }
        catch (error) {
            console.log(error)
        }
    }
    return (
        <div className="py-10 px-20 bg-white">
            <InformacionEmisor emisor={emisor} datosFactura={datosFactura}/>
            <InformacionReceptor receptor={receptor}/>
            <TablaVentaTerceros/>
        </div>
    )
}