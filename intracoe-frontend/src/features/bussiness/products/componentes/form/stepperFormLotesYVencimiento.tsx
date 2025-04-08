import React, { useEffect, useState } from 'react'
import { Almacen, ProductoRequest } from '../../../../../shared/interfaces/interfaces';
import { Checkbox } from 'primereact/checkbox';
import { Calendar } from 'primereact/calendar';
import { Nullable } from 'primereact/ts-helpers';
import { MultiSelect } from 'primereact/multiselect';
import { getAllAlmacenes } from '../../../../../shared/services/tributos/tributos';

interface StepperInformacionGeneralProps {
  formData: ProductoRequest;
  handleChange: any;
}

export const StepperFormLotesYVencimiento: React.FC<StepperInformacionGeneralProps> = ({
  formData,
  handleChange
}) => {
  // Estado local para el Date
  const [date, setDate] = useState<Nullable<Date>>(null);
  const [almacenes, setAlmacenes] = useState<Almacen[]>([])

  // Al montar o cuando cambie formData.fecha_vencimiento, parseamos el string
  useEffect(() => {
    const fv = formData.fecha_vencimiento;
    if (typeof fv === 'string' && fv.includes('/')) {
      const [dd, mm, yyyy] = fv.split('/');
      setDate(new Date(+yyyy, +mm - 1, +dd));
    }
  }, [formData.fecha_vencimiento]);

  useEffect(()=> {
    fetchAlmacenes()
  },[])

  const fetchAlmacenes = async () => {
    try {
      const response = await getAllAlmacenes()
      setAlmacenes(response)
    } catch (error) {
      console.log(error)
    }
  }

  const formatDate = (d: Date) => {
    const dd = String(d.getDate()).padStart(2, '0');
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const yyyy = d.getFullYear();
    return `${yyyy}-${mm}-${dd}`;
  };

  // Firma correcta para CalendarChangeParams
  const onDateChange = (e: any) => {
    const d = e.value as Date;
    setDate(d);
    handleChange({
      target: {
        name: 'fecha_vencimiento',
        value: d ? formatDate(d) : ''
      }
    });
  };

  return (
    <div className='flex flex-col gap-8'>
      <span className='w-full flex'>
        <Checkbox
          onChange={(e) =>
            handleChange({ target: { name: 'maneja_lotes', value: e.checked } })
          }
          checked={formData.maneja_lotes}
        />
        <label htmlFor="maneja_lotes" className="flex pl-2">Maneja lotes</label>
      </span>

      <span className='w-full'>
        <label htmlFor="fecha_vencimiento" className="flex mb-1">
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

      <span className='w-full'>
        <label htmlFor="almacenes" className="flex mb-1">
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
          className="w-full text-start border rounded-md"
        />
      </span>
    </div>
  )
}
