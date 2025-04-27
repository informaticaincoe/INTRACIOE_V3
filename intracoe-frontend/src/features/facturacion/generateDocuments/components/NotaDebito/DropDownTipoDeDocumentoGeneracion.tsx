import { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getAllTiposGeneracionDocumento } from '../../../../../shared/catalogos/services/catalogosServices';

interface DropFownTipoDeDocumentoGeneracionInterface {
  tipoGeneracionFactura: any;
  setTipoGeneracionFactura: any;
}

export const DropFownTipoDeDocumentoGeneracion: React.FC<
  DropFownTipoDeDocumentoGeneracionInterface
> = ({ tipoGeneracionFactura, setTipoGeneracionFactura }) => {
  const [tipoGeneracionDocumentoTempList, seTipoGeneracionDocumentoTempLista] =
    useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoGeneracionDeDocumento();
  }, []);

  const fetchTipoGeneracionDeDocumento = async () => {
    try {
      const response = await getAllTiposGeneracionDocumento();
      console.log('response', response);
      seTipoGeneracionDocumentoTempLista(
        response.map((documento: { descripcion: any; codigo: any }) => ({
          name: documento.descripcion, // Texto que se muestra en la lista
          code: documento.codigo, // Valor que se asigna al seleccionar una opción
        }))
      );
      setTipoGeneracionFactura({
        name: response[0].descripcion, // Texto que se muestra en la lista
        code: response[0].codigo, // Valor que se asigna al seleccionar una opción
      });
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Dropdown
      value={tipoGeneracionFactura} // El valor seleccionado actualmente (ahora es el id del tipo de documento)
      onChange={(e: { value: any }) => setTipoGeneracionFactura(e.value)} // Actualiza el estado con el tipo de documento seleccionado
      options={tipoGeneracionDocumentoTempList} // Las opciones que vienen del API
      optionLabel="name" // Mostrar 'descripcion' de cada opción
      placeholder="Seleccionar tipo de documento"
      className="md:w-14rem font-display w-full text-start"
      filter
    />
  );
};
