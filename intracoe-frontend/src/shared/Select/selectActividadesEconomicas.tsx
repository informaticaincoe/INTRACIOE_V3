import React, { useEffect, useState, HTMLProps } from 'react';
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';
import { ActivitiesData } from '../interfaces/interfaces';
import { getAllActivities } from '../catalogos/services/catalogosServices';
import { GoX } from 'react-icons/go';

interface SelectActividadesEconomicasProps {
  value: any[];
  onChange: (e: {
    target: { name: string; value: (string | number)[] };
  }) => void;
  className?: HTMLProps<HTMLElement>['className'];
  name: string;
}

export const SelectActividadesEconomicas: React.FC<
  SelectActividadesEconomicasProps
> = ({ value, onChange, className, name }) => {
  const [listActividades, setListActividades] = useState<ActivitiesData[]>([]);

  // 1) Carga las actividades desde la API
  useEffect(() => {
    (async () => {
      try {
        const response = await getAllActivities();
        setListActividades(response);
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  useEffect(() => {
    console.log('Selected activities:', value);
  }, [value]);

  // 2) Deriva el array de objetos seleccionados, filtrando por código
  const selectedActivities = listActividades.filter((act) =>
    value.includes(act.id)
  );

  // 3) Función para eliminar una actividad seleccionada
  const handleRemoveActivity = (id: number) => {
    const newValue = value.filter((item) => item !== id);
    onChange({
      target: {
        name,
        value: newValue,
      },
    });
  };

  return (
    <div>
      <MultiSelect
        value={value}
        options={listActividades}
        optionLabel="descripcion" // muestra la descripción en la lista y en los chips
        optionValue="id" // almacena sólo el código en `value`
        placeholder="Seleccionar actividad económica"
        className={`${className} w-full`}
        filter
        maxSelectedLabels={1} // opcional: "+N más"
        panelStyle={{ overflowY: 'auto' }}
        onChange={(e: MultiSelectChangeEvent) => {
          onChange({
            target: {
              name,
              value: e.value,
            },
          });
        }}
      />

      {selectedActivities.length > 0 && (
        <div className="pt-10">
          <strong>Actividades seleccionadas:</strong>
          <div>
            <ul className="bg-body-bg my-4 flex max-h-80 flex-col gap-4 overflow-auto rounded-sm p-5 text-black">
              {selectedActivities.map((act) => (
                <li
                  className="flex w-full justify-between gap-5 rounded-md bg-white p-3"
                  key={act.id} // Usar `id` como clave única
                >
                  <div className="flex items-center gap-2">
                    <button
                      className="text-primary-blue rounded-full p-2 hover:bg-[#DDDFF0]"
                      onClick={() => handleRemoveActivity(act.id)}
                    >
                      <GoX size={24} />
                    </button>
                    <span>{act.descripcion}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
