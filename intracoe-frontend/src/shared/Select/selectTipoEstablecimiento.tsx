import { Dropdown } from 'primereact/dropdown';
import { getAllTiposEstablecimientos } from '../../features/bussiness/configBussiness/services/tiposEstablecimientosService';
import { useEffect, useState } from 'react';

interface SelectedTipoEstablecimientoInterface {
  tipoEstablecimiento: any;
  setTipoEstablecimiento: any;
}

export const SelectTipoEstablecimiento: React.FC<
  SelectedTipoEstablecimientoInterface
> = ({ tipoEstablecimiento, setTipoEstablecimiento }) => {
  const [selectedTipoEstablecimiento, setSelectedTipoEstablecimiento] =
    useState<[]>([]);

  useEffect(() => {
    fetchListaAmbiente();
  }, []);

  const fetchListaAmbiente = async () => {
    try {
      const response = await getAllTiposEstablecimientos();

      const data = response.map(
        (doc: { id: string; descripcion: any; codigo: any }) => ({
          id: doc.id,
          name: doc.descripcion,
          code: doc.codigo,
        })
      );

      setSelectedTipoEstablecimiento(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="justify-content-center flex">
      <Dropdown
        value={tipoEstablecimiento}
        onChange={(e) => setTipoEstablecimiento(e.value)}
        options={selectedTipoEstablecimiento}
        optionLabel="name"
        placeholder="Seleccionar ambiente"
        className="md:w-14rem font-display w-full"
      />
    </div>
  );
};
