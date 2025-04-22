import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import { getAllTiposEstablecimientos } from '../catalogos/services/catalogosServices';

interface SelectedTipoEstablecimientoInterface {
  value: any;
  onChange: (e: {
    target: { name: string; value: (string | number)[] };
  }) => void;
  name: string;
}

export const SelectTipoEstablecimiento: React.FC<
  SelectedTipoEstablecimientoInterface
> = ({ value, onChange, name }) => {
  const [tipoEstablecimiento, setTipoEstablecimiento] = useState<[]>([]);

  useEffect(() => {
    fetchListaAmbiente();
  }, []);

  const fetchListaAmbiente = async () => {
    try {
      const response = await getAllTiposEstablecimientos();
      setTipoEstablecimiento(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={value}
        onChange={(e) =>
          onChange({
            target: {
              name,
              value: e.value,
            },
          })
        }
        options={tipoEstablecimiento}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar ambiente"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
