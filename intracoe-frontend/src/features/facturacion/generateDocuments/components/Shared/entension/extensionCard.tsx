import React from 'react';
import { Input } from '../../../../../../shared/forms/input';

interface ExtensionCardProps {
  nombreResponsable: string;
  setNombreResponsable: any;
  docResponsable: string;
  setDocResponsable: any;
}

export const ExtensionCard: React.FC<ExtensionCardProps> = ({
  nombreResponsable,
  setNombreResponsable,
  docResponsable,
  setDocResponsable,
}) => {
  return (
    <div className="grid grid-cols-[auto_1fr] gap-5">
      <p className="text-start">Nombre responsable:</p>
      <p>
        <Input
          name={'nombreResponsable'}
          value={nombreResponsable}
          onChange={(e) => setNombreResponsable(e.target.value)}
        />
      </p>
      <p className="text-start">Documento responsable:</p>
      <p>
        <Input
          name={'docResponsable'}
          value={docResponsable}
          onChange={(e) => setDocResponsable(e.target.value)}
        />
      </p>
    </div>
  );
};
