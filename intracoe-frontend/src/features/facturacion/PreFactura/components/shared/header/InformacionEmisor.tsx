import { DatosFactura, Emisor } from "../../../interfaces/facturaPdfInterfaces"
import logo from "../../../../../../assets/logo.png"
import React, { useEffect } from "react"
interface InformacionEmisorProps {
    emisor: Emisor,
    datosFactura: DatosFactura

}

export const InformacionEmisor: React.FC<InformacionEmisorProps> = ({ emisor, datosFactura }) => {
    useEffect(() => {
        console.log('datosFactura', datosFactura)
    }, [])
    return (
        <div className="grid grid-cols-5"
        >
            <span className="flex items-center">
                <img src={logo} alt="logo" className="w-full" />
            </span>
            <span className="flex flex-col gap-1 col-span-3">
                <p className="font-semibold">{emisor.nombre}</p>
                <p className="font-semibold">NIT.{emisor.nit}</p>
                <p>{emisor.direccion.complemento}</p>
                <p>Codigo generacion: {datosFactura.codigoGeneracion}</p>
                <p>Numero de control: {datosFactura.numeroControl}</p>
            </span>
            <span style={{
                width: '100%',
                border: '2px solid #ccc',
                borderRadius: '6px',
                padding: '0.5rem',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gridColumnStart: 5
            }}>
                <p>Factura Electronica</p>
                <img style={{ width: '5vw', height: '5vw', margin: '0.5rem 0' }} src="https://upload.wikimedia.org/wikipedia/commons/d/d7/Commons_QR_code.png" alt="qr" />
                <p>Generado: {datosFactura.fechaEmision}</p>
                <p>{datosFactura.horaEmision}</p>
            </span>
        </div>
    )
}