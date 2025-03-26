import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { generarFacturaService } from "../../services/facturavisualizacionServices";
import { InformacionEmisor } from "../../components/shared/header/InformacionEmisor";
import { Emisor } from "../../interfaces/facturaPdfInterfaces";

export const FacturaVisualizacionPage = () => {
    let { id } = useParams();
    const [emisor, setEmisor] = useState<Emisor>()

    useEffect(() => {
        fetchDatosFactura()
    })

    const fetchDatosFactura = async () => {
        try {
            if(id) {
                const response = generarFacturaService(id)
                console.log((await response).emisor)
                console.log((await response).receptor)
                setEmisor((await response).emisor)
            }
        }
        catch (error) {
            console.log(error)
        }
    }
    return (
        <>
            <InformacionEmisor emisor={emisor}/>
        </>
    )
}