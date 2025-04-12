import React, { useEffect, useState, HTMLProps } from 'react';
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';
import { ActivitiesData } from '../interfaces/interfaces';
import { getAllActivities } from '../catalogos/services/catalogosServices';

interface SelectActividadesEconomicasProps {
  value: any[];
  onChange: (e: { target: { name: string; value: (string | number)[] } }) => void;
  className?: HTMLProps<HTMLElement>['className'];
  name: string;
}

export const SelectActividadesEconomicas: React.FC<SelectActividadesEconomicasProps> = ({
  value,
  onChange,
  className,
  name
}) => {
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

  useEffect(()=> {
    console.log("", value)
  },[value])

  // 2) Deriva el array de objetos seleccionados, filtrando por código
  const selectedActivities = listActividades.filter(act =>
    value.includes(act.id)
  );

  return (
    <div>
      <MultiSelect
        value={value}
        options={listActividades}
        optionLabel="descripcion"   // muestra la descripción en la lista y en los chips
        optionValue="id"        // almacena sólo el código en `value`
        placeholder="Seleccionar actividad económica"
        className={`${className} w-full`}
        filter
        maxSelectedLabels={1}       // opcional: "+N más"
        panelStyle={{ overflowY: 'auto' }}
        onChange={(e: MultiSelectChangeEvent) => {
          onChange({
            target: {
              name,
              value: e.value
            }
          });
        }}
      />

      {selectedActivities.length > 0 && (
        <div className="py-5 max-h-40 overflow-auto">
          <strong>Actividades seleccionadas:</strong>
          <ul className="list-inside list-disc px-5 text-black">
            {selectedActivities.map(act => (
              <li key={act.codigo}>{act.descripcion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
