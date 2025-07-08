import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllModelosDeFacturacion } from '../../../../../../../shared/catalogos/services/catalogosServices';
import { getTipoContingencia } from '../../../../services/configuracionFactura/configuracionFacturaService';

interface SelectTipoContingenciaProps {
  setTipoContingencia?: any
  tipoContingencia?: any
}

export const SelectTipoContingencia:React.FC<SelectTipoContingenciaProps> = ({setTipoContingencia, tipoContingencia}) => {
  const [tipoContingencialista, setTipoContingencialista] = useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTiposdeContingencias();
  }, []);

  const fetchTiposdeContingencias = async () => {
    const response = await getTipoContingencia();
    setTipoContingencialista(response);
  };
setTipoContingencia
  return (
    <div className="flex flex-col items-start gap-1">
      <label className="opacity-70">
        Modelo de facturación
      </label>
      <Dropdown
        id={tipoContingencia}
        value={tipoContingencia}
        onChange={(e: { value: any }) => {setTipoContingencia(e.value)}}
        options={tipoContingencialista}
        optionLabel="descripcion"
        optionValue="codigo"
        placeholder="Seleccionar tipo de documento"
        className="md:w-14rem font-display w-full border text-start"
      />
    </div>
  );
};
