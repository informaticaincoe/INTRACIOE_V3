import { Emisor } from '../../../interfaces/facturaPdfInterfaces';
import { TfiEmail } from 'react-icons/tfi';
import { BsTelephone } from 'react-icons/bs';

interface ContactosProps {
  emisor: Emisor;
}

export const Contactos: React.FC<ContactosProps> = ({ emisor }) => {
  return (
    <div className="flex w-full justify-end gap-10 pt-3">
      <p>Contactanos:</p>
      <span className="flex items-center justify-center gap-2">
        <TfiEmail />
        <p>{emisor.correo}</p>
      </span>
      <span className="flex items-center justify-center gap-2">
        <BsTelephone />
        <p>Tel. {emisor.telefono}</p>
      </span>
    </div>
  );
};
