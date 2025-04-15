import React, { useEffect, useState } from 'react';
import {
  Almacen,
  ProductoRequest,
} from '../../../../../shared/interfaces/interfaces';
import { Checkbox } from 'primereact/checkbox';
import { Calendar } from 'primereact/calendar';
import { Nullable } from 'primereact/ts-helpers';
import { MultiSelect } from 'primereact/multiselect';
import { getAllAlmacenes } from '../../../../../shared/services/tributos/tributos';

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  handleChange: any;
}

export const StepperFormLotesYVencimiento: React.FC<
  StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
  // Estado local para el Date
  const [date, setDate] = useState<Nullable<Date>>(null);
  const [almacenes, setAlmacenes] = useState<Almacen[]>([]);

  useEffect(() => {
    fetchAlmacenes();
  }, []);

  const fetchAlmacenes = async () => {
    try {
      const response = await getAllAlmacenes();
      setAlmacenes(response);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const fv = formData.fecha_vencimiento;

    if (typeof fv === 'string' && fv) {
      // Si viene como string "yyyy-mm-dd"
      const [yyyy, mm, dd] = fv.split('-').map(Number);
      setDate(new Date(yyyy, mm - 1, dd));
    } else if (fv instanceof Date) {
      // Si ya es un Date
      setDate(fv);
    } else {
      // Si no hay valor
      setDate(null);
    }
  }, [formData.fecha_vencimiento]);

  // Forma correcta para CalendarChangeParams
  const onDateChange = (e: any) => {
    const selected: Date = e.value;
    setDate(selected);

    if (selected) {
      const yyyy = selected.getFullYear();
      const mm = String(selected.getMonth() + 1).padStart(2, '0');
      const dd = String(selected.getDate()).padStart(2, '0');
      handleChange({
        target: {
          name: 'fecha_vencimiento',
          value: `${yyyy}-${mm}-${dd}`,
        },
      });
    } else {
      handleChange({
        target: { name: 'fecha_vencimiento', value: '' },
      });
    }
  };

  return (
    <div className="flex flex-col gap-8">
      <span className="flex w-full">
        <Checkbox
          onChange={(e) =>
            handleChange({ target: { name: 'maneja_lotes', value: e.checked } })
          }
          checked={formData.maneja_lotes}
        />
        <label htmlFor="maneja_lotes" className="flex pl-2">
          Maneja lotes
        </label>
      </span>

      <span className="w-full">
        <label htmlFor="fecha_vencimiento" className="mb-1 flex">
          Fecha vencimiento
        </label>
        <Calendar
          id="fecha_vencimiento"
          value={date}
          onChange={onDateChange}
          dateFormat="yy-mm-dd"
          showButtonBar
          className="w-full"
        />
      </span>

      <span className="w-full">
        <label htmlFor="almacenes" className="mb-1 flex">
          Almacenes
        </label>
        <MultiSelect
          id="almacenes"
          name="almacenes"
          value={formData.almacenes}
          onChange={(e) =>
            handleChange({ target: { name: 'almacenes', value: e.value } })
          }
          optionValue="id"
          optionLabel="nombre"
          options={almacenes}
          className="w-full rounded-md border text-start"
        />
      </span>
    </div>
  );
};
