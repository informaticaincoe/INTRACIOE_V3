import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllModelosDeFacturacion } from '../../../../../../../shared/catalogos/services/catalogosServices';

interface SelectModeloFacturaProps {
  setTipoModeloFacturacionSeleccionado?: any
  tipoModeloFacturacionSeleccionado?: any
}

export const SelectModeloFactura: React.FC<SelectModeloFacturaProps> = ({ setTipoModeloFacturacionSeleccionado, tipoModeloFacturacionSeleccionado }) => {
  const [selectedModeloFacturacion, setSelectedModeloFacturacion] =
    useState<any>(''); // valor seleccionado
  const [tipoModeloFacturacion, setTipoModeloFacturacion] = useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    const response = await getAllModelosDeFacturacion();
    if (response) {
      setTipoModeloFacturacion(response);
      setSelectedModeloFacturacion(response[0].codigo);
      setTipoModeloFacturacionSeleccionado(response[0].codigo)
    }
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor={selectedModeloFacturacion.codigo} className="opacity-70">
        Modelo de facturación
      </label>
      <Dropdown
        id={selectedModeloFacturacion.codigo}
        value={selectedModeloFacturacion}
        onChange={(e: { value: any }) => { setSelectedModeloFacturacion(e.value), setTipoModeloFacturacionSeleccionado(e.value) }}
        options={tipoModeloFacturacion}
        optionLabel="descripcion"
        optionValue="codigo"
        placeholder="Seleccionar tipo de documento"
        className="md:w-14rem font-display w-full border text-start"
      />
    </div>
  );
};
