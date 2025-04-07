import React, { useState } from 'react'
import { ProductoRequest } from '../../../../../shared/interfaces/interfaces';
import { Input } from '../../../../../shared/forms/input';
import { Checkbox } from 'primereact/checkbox';
import { Calendar } from 'primereact/calendar';
import { Nullable } from 'primereact/ts-helpers';

interface StepperInformacionGeneralProps {
    formData: ProductoRequest;
    handleChange: any;
}

export const StepperFormLotesYVencimiento: React.FC<
    StepperInformacionGeneralProps
> = ({ formData, handleChange }) => {
    const [date, setDate] = useState<Nullable<Date>>(null);

    return (
        <>
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
                    <label htmlFor="tipo_documento" className="flex">
                        Fecha vencimiento
                    </label>
                    <Calendar value={formData.fecha_vencimiento}
                        onChange={(e) =>
                            handleChange({ target: { name: 'fecha_vencimiento', value: e.value } })
                        }
                        dateFormat="dd/mm/yy"
                        showButtonBar
                        className='w-full'
                    />
                </span>
                <span className='w-full'>
                    <label htmlFor="tipo_documento" className="flex">
                        Almacenes
                    </label>
                    <Input
                        type="text"
                        name="tributo"
                        value={formData.almacenes.toString()}
                        onChange={handleChange}
                    />
                </span>
            </div>
        </>
    )
}
