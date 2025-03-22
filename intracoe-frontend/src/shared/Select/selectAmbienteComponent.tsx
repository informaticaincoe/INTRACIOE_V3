import { Dropdown } from 'primereact/dropdown';
import './selectCustomStyle.css';
import { useEffect, useState } from 'react';
import { getAllAmbientes } from '../../features/bussiness/configBussiness/services/ambienteService';

interface SelectAmbienteProps {
  ambiente: any;
  setSelectAmbiente: any;
}

export const SelectAmbienteComponent: React.FC<SelectAmbienteProps> = ({
  ambiente,
  setSelectAmbiente,
}) => {
  const [selectedAmbiente, setSelectedAmbiente] = useState<[]>([]);

  useEffect(() => {
    fetchListaAmbiente();
  }, []);

  const fetchListaAmbiente = async () => {
    try {
      const response = await getAllAmbientes();

      const data = response.map(
        (doc: { id: string; descripcion: any; codigo: any }) => ({
          id: doc.id,
          name: doc.descripcion,
          code: doc.codigo,
        })
      );

      setSelectedAmbiente(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={ambiente}
        onChange={(e) => setSelectAmbiente(e.value)}
        options={selectedAmbiente}
        optionLabel="name"
        placeholder="Seleccionar ambiente"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
