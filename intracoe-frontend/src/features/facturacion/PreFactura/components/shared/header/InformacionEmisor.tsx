import { DatosFactura, Emisor } from '../../../interfaces/facturaPdfInterfaces';
import logo from '../../../../../../assets/logo.png';
import React, { useEffect, useState } from 'react';
import { DTEByCode } from '../../../../../../shared/services/DTEServices';
import { QRCode } from 'antd';
interface InformacionEmisorProps {
  emisor: Emisor;
  datosFactura: DatosFactura;
  qrCode: string;
}

export const InformacionEmisor: React.FC<InformacionEmisorProps> = ({
  emisor,
  datosFactura,
  qrCode,
}) => {
  const [nombreDte, setNombreDte] = useState<string>('');
  useEffect(() => {
    if (datosFactura.tipoDte) fetchTipoDTE();
    console.log(qrCode);
  }, [datosFactura.tipoDte]);

  const fetchTipoDTE = async () => {
    const response = await DTEByCode(datosFactura.tipoDte);
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
        <p>Codigo generacion: {datosFactura.codigoGeneracion.toUpperCase()}</p>
        <p>Numero de control: {datosFactura.numeroControl}</p>
        <p>Sello: {datosFactura.selloRemision}</p>
      </span>
      <span className="border-border-color col-start-5 flex w-full flex-col items-center rounded-md border-2 p-2">
        <p>{nombreDte}</p>
        {/* <img
          style={{ width: '5vw', height: '5vw', margin: '0.5rem 0' }}
          src="https://upload.wikimedia.org/wikipedia/commons/d/d7/Commons_QR_code.png"
          alt="qr"
        /> */}
        <div style={{ width: '7vw', height: '7vw', margin: '0' }}>
          <QRCode
            value={qrCode || '-'}
            style={{ width: '100%', height: '100%', margin: '0' }}
          />
        </div>
        <p>Generado: {datosFactura.fechaEmision}</p>
        <p>{datosFactura.horaEmision}</p>
      </span>
    </div>
  );
};
