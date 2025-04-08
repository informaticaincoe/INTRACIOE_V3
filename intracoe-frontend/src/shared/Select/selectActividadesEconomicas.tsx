import React, { HTMLProps, useEffect, useState } from 'react';
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';
import { ActivitiesData } from '../interfaces/interfaces';
import { getAllActivities } from '../../features/facturacion/activities/services/activitiesServices';
import { EmisorInterface } from '../interfaces/interfaces';

interface SelectActividadesEconomicasProps {
  value: any;
  onChange: any;
  className?: HTMLProps<HTMLElement>['className'];
  name:string
}

export const SelectActividadesEconomicas: React.FC<SelectActividadesEconomicasProps> = ({
  value,
  onChange,
  className,
  name
}) => {
  const [listActividades, setListActividades] = useState<ActivitiesData[]>([]);

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

  return (
    <div>
      <MultiSelect
        value={value}
        options={listActividades}
        optionLabel="descripcion"
        placeholder="Seleccionar actividad económica"
        className={`${className} w-contain`}
        filter
        onChange={(e: MultiSelectChangeEvent) =>
          onChange({
            target: {
              name: name,
              value: e.value
            }
          })
        }
      />

      {value.length > 0 && (
        <div className="py-5">
          <strong>Actividades seleccionadas:</strong>
          <ul>
            {value.actividades_economicas.map((act: { codigo: React.Key | null | undefined; descripcion: string | number | bigint | boolean | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | React.ReactPortal | Promise<string | number | bigint | boolean | React.ReactPortal | React.ReactElement<unknown, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | null | undefined> | null | undefined; }) => (
              <li
                key={act.codigo}
                className="list-inside list-disc px-5 text-black"
              >
                {act.descripcion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
