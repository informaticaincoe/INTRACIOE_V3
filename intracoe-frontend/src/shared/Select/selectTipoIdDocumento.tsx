import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllTipoIdReceptor } from '../../features/bussiness/configBussiness/services/tipoIdReceptor';

interface SelectedTipoIdDocumentoInterface {
  setTipoIdDocumento: any;
  tipoIdDocumento: any;
}

export const SelectTipoIdDocumento: React.FC<
  SelectedTipoIdDocumentoInterface
> = ({ setTipoIdDocumento, tipoIdDocumento }) => {
  const [tipoDocId, setTipoDocId] = useState<any[]>([]);

  useEffect(() => {
    fetchTipoDocId();
  }, []);

  const fetchTipoDocId = async () => {
    try {
      const response = await getAllTipoIdReceptor();

      const data = response.map(
        (doc: { id: string; descripcion: any; codigo: any }) => ({
          id: doc.id,
          name: doc.descripcion, // Asignar 'descripcion' a 'label'
          code: doc.codigo, // Asignar 'codigo' a 'value'
        })
      );

      if (data.length > 0) {
        setTipoDocId(data);
        console.log(data[0]);
        setTipoIdDocumento(data[0]); // Establecer el valor del primer elemento como seleccionado
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={tipoIdDocumento}
        onChange={(e) => setTipoIdDocumento(e.value)}
        options={tipoDocId}
        optionLabel="name"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
