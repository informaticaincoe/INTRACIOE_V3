import { useEffect, useState } from 'react';
import {
  Receptor,
  TipoIdentificacion,
} from '../../../interfaces/facturaPdfInterfaces';
import { tipoIdReceptor } from '../../../../../../shared/services/receptor/receptorServices';

interface InformacionReceptorProps {
  receptor: Receptor;
}

export const InformacionReceptor: React.FC<InformacionReceptorProps> = ({
  receptor,
}) => {
  const [tipoIdDocumento, setTipoDocumento] =
    useState<TipoIdentificacion | null>(null);

  useEffect(() => {
    if (receptor.tipoDocumento) {
      fetchTipoID();
    }
  }, [receptor.tipoDocumento]);

  const fetchTipoID = async () => {
    if (receptor.tipoDocumento) {
      try {
        const aux = await tipoIdReceptor(receptor.tipoDocumento);
        setTipoDocumento(aux);
      } catch (error) {
        console.log(error);
      }
    }
  };
  return (
    <div className="pt-8">
      <h1 className="font-bold uppercase">Receptor</h1>
      <div className="border-border-color grid grid-cols-[auto_1fr] gap-x-5 rounded-md border-2 p-5 text-start">
        <div className="flex flex-col gap-1.5 opacity-70">
          <p>Nombre o razon social:</p>
          <p>Documento identificacion:</p>
          <p>Correo electronico:</p>
          <p>telefono:</p>
          <p>direccion:</p>
        </div>
        <div className="flex flex-col gap-1.5">
          <p>{receptor.nombre}</p>
          {receptor.numDocumento && (
            <p>
              {receptor.numDocumento} ({tipoIdDocumento?.descripcion})
            </p>
          )}
          {receptor.nit && <p>{receptor.nit} (nit)</p>}
          <p>{receptor.correo}</p>
          <p>{receptor.telefono}</p>
          <p>{receptor.direccion.complemento}</p>
        </div>
      </div>
    </div>
  );
};
