import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllModelosDeFacturacion } from '../../../../services/configuracionFactura/configuracionFacturaService';

export const SelectModeloFactura = () => {
  const [selectedModeloFacturacion, setSelectedModeloFacturacion] =
    useState<any>(''); // valor seleccionado
  const [tipoModeloFacturacion, setTipoModeloFacturacion] = useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    const response = await getAllModelosDeFacturacion()
    setTipoModeloFacturacion(response);
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor={selectedModeloFacturacion.codigo} className="opacity-70">
        Modelo de facturación {selectedModeloFacturacion.codigo}
      </label>
      <Dropdown
        id={selectedModeloFacturacion.codigo}
        value={selectedModeloFacturacion}
        onChange={(e: { value: any }) => setSelectedModeloFacturacion(e.value)}
        options={tipoModeloFacturacion}
        optionLabel="descripcion"
        optionValue="codigo"
        placeholder="Seleccionar tipo de documento"
        className="md:w-14rem font-display w-full text-start"
      />
    </div>
  );
};
