import React, { useEffect, useRef, useState } from 'react'
import { Input } from '../../../../shared/forms/input'
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast'
import { useNavigate, useParams } from 'react-router'
import { FaCheckCircle } from 'react-icons/fa'
import { IoMdCloseCircle } from 'react-icons/io'
import { Title } from '../../../../shared/text/title'
import { CompraInterface } from '../interfaces/comprasInterfaces'
import { addCompra, getComprasById, updateComprasById } from '../services/comprasServices'
import { RadioButton } from 'primereact/radiobutton'
import dayjs from 'dayjs'
import { CiCalendar } from 'react-icons/ci'
import { Calendar } from 'primereact/calendar'

export const ComprasNewEdit = () => {
    let params = useParams();
    const toastRef = useRef<CustomToastRef>(null);
    const navigate = useNavigate();
    const [formData, setFormData] = useState<CompraInterface>({
        id: 0,
        proveedor: 0,
        fecha: "",
        total: 0,
        estado: 'Pendiente',
    })

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
        if (params.id)
            fetchDataEdit()
    }, [])

    const fetchDataEdit = async () => {
        if (params.id) {
            try {
                const response = await getComprasById(params.id);

                if (response && response.id) {
                    setFormData(response);
                } else {
                    // Si la respuesta no es válida, podemos establecer valores predeterminados
                    setFormData({
                        id: 0,
                        proveedor: 0,
                        fecha: "",
                        total: 0,
                        estado: 'Pendiente',
                    });
                }
                console.log(response);
            } catch (error) {
                console.log(error);
            }
        }
    };

    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSendForm = async () => {
        if (params.id) {
            try {
                const response = await updateComprasById(params.id, formData)
                console.log(response)
                handleAccion(
                    'success',
                    <FaCheckCircle size={38} />,
                    'Proveedor actualizado con exito'
                );

                setTimeout(() => {
                    navigate('/compras/');
                }, 2000);
            } catch (error) {
                handleAccion(
                    'error',
                    <IoMdCloseCircle size={38} />,
                    'Error al actualizar el proveedor'
                );
            }
        }
        else {
            try {
                const response = await addCompra(formData)
                console.log(response)
                handleAccion(
                    'success',
                    <FaCheckCircle size={38} />,
                    'proveedor creado con exito'
                );

                setTimeout(() => {
                    navigate('/compras/');
                }, 2000);
            } catch (error) {
                handleAccion(
                    'error',
                    <IoMdCloseCircle size={38} />,
                    'Error al crear el proveedor'
                );
            }
        }
    }

    return (
        <>
            <CustomToast ref={toastRef} />

            <Title text={`${params.id ? ' Editar movimiento' : 'Nuevo movimiento'} `} />
            <div className='bg-white rounded-md p-10 my-10 mx-[20%]'>
                <div>
                    <form action="" className='flex flex-col text-start gap-6'>
                        <span>
                            <label htmlFor="">Proveedor</label>
                            <Input name="proveedor" value={formData.proveedor.toString()} onChange={handleChange} />
                        </span>
                        <span className='flex flex-col text-start'>
                            <label htmlFor="">Fecha</label>
                            <Calendar
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
                                        inputId="Pendiente"
                                        name="estado"
                                        value="Pendiente"
                                        onChange={handleChange}
                                        checked={formData?.estado === 'Pendiente'}
                                    />
                                    <label htmlFor="entrada" className="ml-2">Entrada</label>
                                </div>
                                <div className="flex align-items-center">
                                    <RadioButton
                                        inputId="Pagado"
                                        name="estado"
                                        value="Pagado"
                                        onChange={handleChange}
                                        checked={formData?.estado === 'Pagado'}
                                    />
                                    <label htmlFor="salida" className="ml-2">Salida</label>
                                </div>
                                <div className="flex align-items-center">
                                    <RadioButton
                                        inputId="Cancelado"
                                        name="estado"
                                        value="Cancelado"
                                        onChange={handleChange}
                                        checked={formData?.estado === 'Cancelado'}
                                    />
                                    <label htmlFor="salida" className="ml-2">Salida</label>
                                </div>
                            </div>
                        </span>

                    </form>
                    <div className='w-full flex justify-start pt-5'>
                        <button className='bg-primary-blue text-white rounded-md py-2 px-7' onClick={handleSendForm}>Guardar</button>
                    </div>
                </div>
            </div>
        </>
    )
}
