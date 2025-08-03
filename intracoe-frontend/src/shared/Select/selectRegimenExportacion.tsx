import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllTipoDomicilioFiscal } from '../catalogos/services/catalogosServices';

interface SelectRegimenExportacionProps {
  value: any;
  onChange: any;
  className?: HTMLProps<HTMLElement>['className'];
  name: string;
}

export const SelectRegimenExportacionComponent: React.FC<SelectRegimenExportacionProps> = ({
  value,
  onChange,
  className,
  name,
}) => {
  const [regimen, setRegimen] = useState<[]>([]);

  useEffect(() => {
    fetchListaregimen();
  }, []);

  const fetchListaregimen = async () => {
    try {
      const response = await getAllTipoDomicilioFiscal();
      console.log(response);
      setRegimen(response);
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
        options={regimen}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar regimen"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
