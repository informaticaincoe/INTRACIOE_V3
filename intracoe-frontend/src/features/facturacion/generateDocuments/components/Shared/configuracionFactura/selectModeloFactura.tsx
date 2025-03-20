import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';

const modelosFacturacion = [
  {
    id: 1,
    codigo: 1,
    descripcion: 'Modelo Facturación diferido',
  },
  {
    id: 2,
    codigo: 2,
    descripcion: 'Modelo Facturación previo',
  },
];

export const SelectModeloFactura = () => {
  const [selectedModeloFacturacion, setSelectedModeloFacturacion] =
    useState<any>(''); // valor seleccionado
  const [tipoModeloFacturacion, setTipoModeloFacturacion] = useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    setTipoModeloFacturacion(modelosFacturacion);
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor={selectedModeloFacturacion.id} className="opacity-70">
        Tipo de documento
      </label>
      <Dropdown
        id={selectedModeloFacturacion.id}
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
