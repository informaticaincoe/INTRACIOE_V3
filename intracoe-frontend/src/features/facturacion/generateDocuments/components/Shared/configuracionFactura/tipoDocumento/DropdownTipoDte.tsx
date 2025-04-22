import { Dropdown } from 'primereact/dropdown';
import { useEffect } from 'react';

interface SeccionconfiguracionFacturaInterface {
  tipoDocumento: any;
  setTipoDocumento: any;
  setTipoDocumentoSelected: any;
  tipoDocumentoSelected: any;
}

export const DropDownTipoDte: React.FC<
  SeccionconfiguracionFacturaInterface
> = ({
  tipoDocumento,
  setTipoDocumento,
  setTipoDocumentoSelected,
  tipoDocumentoSelected,
}) => {
  return (
    <Dropdown
      value={tipoDocumentoSelected} // El valor seleccionado actualmente (ahora es el id del tipo de documento)
      onChange={(e: { value: any }) => setTipoDocumentoSelected(e.value)} // Actualiza el estado con el tipo de documento seleccionado
      options={tipoDocumento} // Las opciones que vienen del API
      optionLabel="descripcion" // Mostrar 'descripcion' de cada opción
      optionValue="codigo"
      placeholder="Seleccionar tipo de documento"
      className="md:w-14rem font-display w-full text-start"
      filter
    />
  );
};
