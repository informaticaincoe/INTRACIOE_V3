import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllTipoTransmision } from '../../../../services/configuracionFactura/configuracionFacturaService';

export const SelectTipoTransmisión = () => {
  const [selectedTipoTransmision, setSelectedTipoTransmision] =
    useState<any>(''); // valor seleccionado
  const [tipoTransmisionTempLista, setTipoTransmisionTempLista] = useState<
    any[]
  >([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    const response = await getAllTipoTransmision()
    setTipoTransmisionTempLista(response);
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor={selectedTipoTransmision.id} className="opacity-70">
        Tipo transmisión
      </label>
      <Dropdown
        id={selectedTipoTransmision.id}
        value={selectedTipoTransmision}
        onChange={(e: { value: any }) => setSelectedTipoTransmision(e.value)}
        options={tipoTransmisionTempLista}
        optionLabel="descripcion"
        optionValue="codigo"
        placeholder="Seleccionar tipo de documento"
        className="md:w-14rem font-display w-full text-start"
      />
    </div>
  );
};
