import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllTipoTransmision } from '../../../../../../../shared/catalogos/services/catalogosServices';

interface SelectTipoTransmisionProp {
  setTipoTransmision: (value: any) => void;
  tipoTransmision: string;
}

export const SelectTipoTransmision: React.FC<SelectTipoTransmisionProp> = ({
  setTipoTransmision,
  tipoTransmision,
}) => {
  const [tipoTransmisionTempLista, setTipoTransmisionTempLista] = useState<
    any[]
  >([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    const response = await getAllTipoTransmision();
    setTipoTransmisionTempLista(response);
    setTipoTransmision(response[0].id);
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor="tipoTransmision" className="opacity-70">
        Tipo transmisión
      </label>
      <Dropdown
        id={tipoTransmision}
        value={tipoTransmision}
        onChange={(e: { value: any }) => setTipoTransmision(e.value)}
        options={tipoTransmisionTempLista}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar tipo de documento"
        className="md:w-14rem font-display w-full text-start"
      />
    </div>
  );
};
