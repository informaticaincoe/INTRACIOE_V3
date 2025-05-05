import React, { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { ProveedorInterface } from '../../../proveedores/interfaces/proveedoresInterfaces';
import { Dropdown } from 'primereact/dropdown';
import { Calendar } from 'primereact/calendar';
import { CiCalendar } from 'react-icons/ci';
import dayjs from 'dayjs';
import { Input } from '../../../../../shared/forms/input';
import { RadioButton } from 'primereact/radiobutton';
import { getAllProveedores } from '../../../proveedores/services/proveedoresServices';

interface SteppCrearCompraProps {
    formData: any,
    handleChange: any
}

export const SteppCrearCompra: React.FC<SteppCrearCompraProps> = ({ formData, handleChange }) => {
    let params = useParams();
    const toastRef = useRef<CustomToastRef>(null);
    const [proveedoresLista, setProveedoresLista] = useState<ProveedorInterface[] | undefined>([])

    const handleAccion = (
        severity: ToastSeverity,
        icon: any,
        summary: string
    ) => {
        toastRef.current?.show({
            severity: severity,
            summary: summary,
            icon: icon,
            life: 2000,
        });
    };

    useEffect(() => {
        fetchProveedores()
    }, [])


    const fetchProveedores = async () => {
        try {
            const response = await getAllProveedores();
            setProveedoresLista(response)
        }
        catch {

        }
    }

    return (
        <>
            <CustomToast ref={toastRef} />
            <div>
                <form action="" className='flex flex-col text-start gap-6'>
                    <span>
                        <label htmlFor="">Proveedor</label>
                        <Dropdown
                            name="proveedor"
                            value={formData?.proveedor}
                            onChange={(e) =>
                                handleChange({ target: { name: 'proveedor', value: e.value } })
                            }
                            options={proveedoresLista}
                            optionLabel="nombre"
                            optionValue="id"
                            placeholder="Seleccionar proveedor"
                            className="md:w-14rem w-full text-start"
                        />
                    </span>
                    <span className='flex flex-col text-start'>
                        <label htmlFor="">Fecha</label>
                        <Calendar
                            disabled
                            name="fecha"
                            value={formData?.fecha ? dayjs(formData.fecha).toDate() : null} // Convertimos el valor a un objeto Date
                            onChange={handleChange}
                            dateFormat="dd-mm-yy" // Formato de fecha que desees
                            showIcon
                            showTime
                            icon={<CiCalendar size={20} color="rgba(0,0,0,0.5)" />}
                            iconPos="left"
                        />
                    </span>
                    <span>
                        <label htmlFor="">Total</label>
                        <Input type='number' name="total" value={(formData.total ?? 0).toString()} onChange={handleChange} />
                    </span>
                    <span className='flex flex-col text-start w-full'>
                        <label htmlFor="">Estado</label>
                        <div className='flex gap-5'>
                            <div className="flex align-items-center">
                                <RadioButton
                                    inputId="Pagado"
                                    name="estado"
                                    value="Pagado"
                                    onChange={handleChange}
                                    checked={formData?.estado === 'Pagado'}
                                />
                                <label htmlFor="salida" className="ml-2">Pagado</label>
                            </div>
                            <div className="flex align-items-center">
                                <RadioButton
                                    inputId="Pendiente"
                                    name="estado"
                                    value="Pendiente"
                                    onChange={handleChange}
                                    checked={formData?.estado === 'Pendiente'}
                                />
                                <label htmlFor="entrada" className="ml-2">Pendiente</label>
                            </div>
                            <div className="flex align-items-center">
                                <RadioButton
                                    inputId="Cancelado"
                                    name="estado"
                                    value="Cancelado"
                                    onChange={handleChange}
                                    checked={formData?.estado === 'Cancelado'}
                                />
                                <label htmlFor="salida" className="ml-2">Cancelado</label>
                            </div>
                        </div>
                    </span>
                </form>
            </div>
        </>
    )
}
