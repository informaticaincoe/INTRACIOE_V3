import { Dropdown } from 'primereact/dropdown';
import { HTMLProps, useEffect, useState } from 'react';
import { getAllRegimenFiscal } from '../catalogos/services/catalogosServices';

interface SelectRegimenExportacionProps {
  regimenSelecionado: any;
  setRegimenSelecionado: any;
  className?: HTMLProps<HTMLElement>['className'];
}

export const SelectRegimenExportacionComponent: React.FC<SelectRegimenExportacionProps> = ({
  regimenSelecionado,
  setRegimenSelecionado,
  className,
}) => {
  const [regimen, setRegimen] = useState<[]>([]);

  useEffect(() => {
    fetchListaregimen();
  }, []);

  const fetchListaregimen = async () => {
    try {
      const response = await getAllRegimenFiscal();
      console.log(response);
      setRegimen(response);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex flex-col items-start gap-1">
      <label htmlFor="tipoTransmision" className="opacity-70">
        Regimen
      </label>
      <Dropdown
        value={regimenSelecionado}
        onChange={(e) =>
          setRegimenSelecionado(e.value)
        }
        options={regimen}
        optionLabel="descripcion"
        optionValue="id"
        placeholder="Seleccionar regimen"
        className="md:w-14rem font-display w-full text-start"
      />
    </div>
  );
};
