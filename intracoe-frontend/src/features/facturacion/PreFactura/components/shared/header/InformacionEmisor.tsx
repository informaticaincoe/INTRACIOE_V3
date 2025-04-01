import { DatosFactura, Emisor } from '../../../interfaces/facturaPdfInterfaces';
import logo from '../../../../../../assets/logo.png';
import React, { useEffect, useState } from 'react';
import { DTEByCode } from '../../../../../../shared/services/DTEServices';
interface InformacionEmisorProps {
  emisor: Emisor;
  datosFactura: DatosFactura;
}

export const InformacionEmisor: React.FC<InformacionEmisorProps> = ({
  emisor,
  datosFactura,
}) => {
  const [nombreDte, setNombreDte] = useState<string>('');
  useEffect(() => {
    if (datosFactura.tipoDte) fetchTipoDTE();
  }, [datosFactura.tipoDte]);

  const fetchTipoDTE = async () => {
    const response = await DTEByCode(datosFactura.tipoDte);
    console.log('NOMBRE DTE', response);
    setNombreDte(response.descripcion);
  };

  return (
    <div className="grid grid-cols-5">
      <span className="flex items-center">
        <img src={logo} alt="logo" className="w-full" />
      </span>
      <span className="col-span-3 flex flex-col gap-1 px-10">
        <p className="font-semibold">{emisor.nombre}</p>
        <p className="font-semibold">NIT.{emisor.nit}</p>
        <p>{emisor.direccion.complemento}</p>
        <p>Codigo generacion: {datosFactura.codigoGeneracion}</p>
        <p>Numero de control: {datosFactura.numeroControl}</p>
        <p>Sello: {datosFactura.selloRemision}</p>
      </span>
      <span className="border-border-color col-start-5 flex w-full flex-col items-center rounded-md border-2 p-2">
        <p>{nombreDte}</p>
        <img
          style={{ width: '5vw', height: '5vw', margin: '0.5rem 0' }}
          src="https://upload.wikimedia.org/wikipedia/commons/d/d7/Commons_QR_code.png"
          alt="qr"
        />
        <p>Generado: {datosFactura.fechaEmision}</p>
        <p>{datosFactura.horaEmision}</p>
      </span>
    </div>
  );
};
