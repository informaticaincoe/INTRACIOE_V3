import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllAmbientes } from '../catalogos/services/catalogosServices';

interface SelectAmbienteProps {
  value: any;
  onChange: (e: {
    target: { name: string; value: (string | number)[] };
  }) => void;
  className?: HTMLProps<HTMLElement>['className'];
  name: string;
}

export const SelectAmbienteComponent: React.FC<SelectAmbienteProps> = ({
  value,
  onChange,
  className,
  name,
}) => {
  const [ambiente, setAmbiente] = useState<[]>([]);

  useEffect(() => {
    fetchListaAmbiente();
  }, []);

  const fetchListaAmbiente = async () => {
    try {
      const response = await getAllAmbientes();
      console.log(response);
      setAmbiente(response);
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
        options={ambiente}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar ambiente"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
