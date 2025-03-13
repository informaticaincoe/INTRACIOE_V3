import { Dropdown } from 'primereact/dropdown';
import { useState } from 'react';

interface SelectedTipoEstablecimientoInterface {
  tipoEstablecimiento: any;
  setTipoEstablecimiento: any;
}

export const SelectTipoEstablecimiento: React.FC<
  SelectedTipoEstablecimientoInterface
> = ({ tipoEstablecimiento, setTipoEstablecimiento }) => {
  const establecimientos = [
    { name: 'Sucursal o agencia', code: '1' },
    { name: 'Casa matriz', code: '2' },
    { name: 'Bodega', code: '3' },
    { name: 'Patio', code: '4' },
  ];

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={tipoEstablecimiento}
        onChange={(e) => setTipoEstablecimiento(e.value)}
        options={establecimientos}
        optionLabel="name"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
        filter
      />
    </div>
  );
};
