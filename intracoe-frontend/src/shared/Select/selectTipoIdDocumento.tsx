import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllTipoIdReceptor } from '../../features/bussiness/configBussiness/services/tipoIdReceptor';

interface SelectedTipoIdDocumentoInterface {
  onChange: any;
  value: any;
  name: any;
}

export const SelectTipoIdDocumento: React.FC<
  SelectedTipoIdDocumentoInterface
> = ({ onChange, value, name }) => {
  const [tipoDocId, setTipoDocId] = useState<any[]>([]);

  useEffect(() => {
    fetchTipoDocId();
  }, []);

  const fetchTipoDocId = async () => {
    try {
      const response = await getAllTipoIdReceptor();
      console.log('response, response');
      setTipoDocId(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={value}
        onChange={(e) => onChange({ target: { name: name, value: e.value } })}
        options={tipoDocId}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar tipo de establecimiento"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
