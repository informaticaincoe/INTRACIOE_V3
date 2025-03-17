import { Dropdown } from 'primereact/dropdown';
import { useEffect, useState } from 'react';
import './selectCustomStyle.css';
import { getAllActivities } from '../../features/facturacion/activities/services/activitiesServices';
import { ActivitiesData } from '../../features/facturacion/activities/interfaces/activitiesData';
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';

interface selectActividadesEconomicasInterface {
  actividades: ActivitiesData[]; // Asegúrate de que actividades sea un array de objetos ActivitiesData
  setActividades: (value: ActivitiesData) => void;
}

export const SelectActividadesEconomicas: React.FC<
  selectActividadesEconomicasInterface
> = ({ actividades, setActividades }) => {
  const [listActividades, setListSetActividades] = useState<ActivitiesData[]>(
    []
  );

  useEffect(() => {
    fetchActividadesList();
  }, []);

  const fetchActividadesList = async () => {
    try {
      const response = await getAllActivities();

      const data = response.map(
        (doc: { id: string; descripcion: any; codigo: any }) => ({
          id: doc.id,
          descripcion: doc.descripcion,
          code: doc.codigo,
        })
      );
      setListSetActividades(data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <div className="justify-content-center flex">
        <MultiSelect
          value={actividades}
          onChange={(e: MultiSelectChangeEvent) => setActividades(e.value)}
          options={listActividades}
          optionLabel="descripcion"
          placeholder="Seleccionar actividad economica"
          className="md:w-20rem w-full"
          filter
        />
      </div>
      {actividades.length > 0 && (
        <div className="py-5">
          <strong>Actividades seleccionadas:</strong>
          <ul>
            {actividades.map((actividad) => (
              <li
                key={actividad.codigo} // Usamos el código para que sea único
                className="list-inside list-disc px-5 text-black"
              >
                {actividad.descripcion}{' '}
                {/* Mostrar la descripción de la actividad */}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
