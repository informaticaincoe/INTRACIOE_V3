import { DatosFactura, Emisor } from "../../../interfaces/facturaPdfInterfaces"
import logo from "../../../../../../assets/logo.png"
import { useEffect } from "react"

interface InformacionEmisorProps {
    emisor: Emisor,
    datosFactura: DatosFactura

}

export const InformacionEmisor: React.FC<InformacionEmisorProps> = ({ emisor, datosFactura }) => {
    useEffect(() => {
        console.log('datosFactura', datosFactura)
    }, [])
    return (
        <div className="grid grid-cols-[15%_70%_15%]">
            <span className="flex items-center">
                <img src={logo} alt="logo" className="w-full" />
            </span>
            <span className="flex flex-col gap-1">
                <p className="font-semibold">{emisor.nombre}</p>
                <p className="font-semibold">NIT.{emisor.nit}</p>
                <p>{emisor.direccion.complemento}</p>
                <p>Codigo generacion: {datosFactura.codigoGeneracion}</p>
                <p>Numero de control: {datosFactura.numeroControl}</p>
            </span>
            <span className="">
                <span className="border-2  border-border-color rounded-md flex flex-col justify-center items-center">
                  <p className="font-bold">Factura Electronica</p>
                  <img className="size-24" src="https://upload.wikimedia.org/wikipedia/commons/d/d7/Commons_QR_code.png" alt="qr" />  
                  <p>Generado: {datosFactura.fechaEmision}</p>
                  <p>{datosFactura.horaEmision}</p>
                </span>
            </span>
        </div>
    )
}