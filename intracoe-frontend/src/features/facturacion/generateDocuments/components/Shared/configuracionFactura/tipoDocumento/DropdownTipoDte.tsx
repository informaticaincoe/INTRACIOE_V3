import { useEffect, useState } from 'react';
import { Dropdown } from 'primereact/dropdown';
import { getAllTipoDte } from '../../../../services/configuracionFactura/configuracionFacturaService';

interface SeccionconfiguracionFacturaInterface {
  tipoDocumento: any;
  setTipoDocumento: any;
}

export const DropDownTipoDte: React.FC<
  SeccionconfiguracionFacturaInterface
> = ({ tipoDocumento, setTipoDocumento }) => {
  // const [selectedTipoDte, setSelectedTipoDte] = useState<any>(''); // valor seleccionado
  const [tipoDteTempList, setTipoDteTempLista] = useState<any[]>([]); // Lista de tipos de documentos

  useEffect(() => {
    fetchTipoDte();
  }, []);

  const fetchTipoDte = async () => {
    try {
      const response = await getAllTipoDte();
      console.log("response", response)
      setTipoDteTempLista(
        response.map((documento: { descripcion: any; codigo: any }) => ({
          name: documento.descripcion, // Texto que se muestra en la lista
          code: documento.codigo, // Valor que se asigna al seleccionar una opción
        }))
      );
      setTipoDocumento({
        name: response[0].descripcion, // Texto que se muestra en la lista
        code: response[0].codigo, // Valor que se asigna al seleccionar una opción
    });

    } catch (error) {
      console.log(error);
    }
  };

  return (

    <Dropdown
      value={tipoDocumento} // El valor seleccionado actualmente (ahora es el id del tipo de documento)
      onChange={(e: { value: any }) => setTipoDocumento(e.value)} // Actualiza el estado con el tipo de documento seleccionado
      options={tipoDteTempList} // Las opciones que vienen del API
      optionLabel="name" // Mostrar 'descripcion' de cada opción
      placeholder="Seleccionar tipo de documento"
      className="md:w-14rem font-display w-full text-start"
      filter
    />
  );
};
