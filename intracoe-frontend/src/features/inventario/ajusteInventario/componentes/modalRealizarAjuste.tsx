import { Dialog } from 'primereact/dialog'
import React, { useEffect, useRef, useState } from 'react'
import { addAjusteMovimientoInventario } from '../services/ajusteInventarioServices'
import { movimientoInterface } from '../../movimientoInventario/interfaces/movimientoInvetarioInterface'
import { Input } from '../../../../shared/forms/input'
import { Almacen, ProductoResponse } from '../../../../shared/interfaces/interfaces'
import { getAllProducts } from '../../../../shared/services/productos/productosServices'
import { Dropdown } from 'primereact/dropdown'
import { getAllAlmacenes } from '../../../../shared/services/tributos/tributos'
import { Calendar } from 'primereact/calendar'
import dayjs from 'dayjs'
import { CiCalendar } from 'react-icons/ci'
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast'
import { useNavigate } from 'react-router'
import { FaCheckCircle } from 'react-icons/fa'
import { IoMdCloseCircle } from 'react-icons/io'

interface ModalRealizarAjusteoProp {
    data: movimientoInterface,
    visible: boolean,
    setVisible: any
}

export const ModalRealizarAjuste: React.FC<ModalRealizarAjusteoProp> = ({ data, visible, setVisible }) => {
    const [productosLista, setProductosLista] = useState<ProductoResponse[]>([])
    const [almacenLista, setAlmacenLista] = useState<Almacen[]>([])
    const toastRef = useRef<CustomToastRef>(null);
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        producto: data.producto ?? 0,
        almacen: data.almacen ?? 0,
        cantidad_ajustada: data.cantidad,
        motivo: "",
        fecha: new Date(),
        usuario: ""
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

    const handleChange = (e: any) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    useEffect(() => {
        fetchProductos()
        fetchAlmacenes()
    }, [])

    const fetchProductos = async () => {
        try {
            const response = await getAllProducts()
            setProductosLista(response)
        }
        catch (error) {
            console.log(error)
        }
    }

    const fetchAlmacenes = async () => {
        try {
            const response = await getAllAlmacenes()
            setAlmacenLista(response)
        }
        catch (error) {
            console.log(error)
        }
    }

    const saveAjuste = async () => {
        console.log("Ajuste inventario:", formData)
        try {
            const response = await addAjusteMovimientoInventario(formData)
            console.log(response)

            handleAccion(
                'success',
                <FaCheckCircle size={38} />,
                'Ajuste de movimiento de inventario realizado con exito'
            );
            setTimeout(() => {
                navigate('/ajuste-inventario/');
            }, 2000);

        }
        catch (error) {
            console.log(error)
            handleAccion(
                'error',
                <IoMdCloseCircle size={38} />,
                'Error al crear ajuste de movimiento de inventario'
            );
        }

    }

    return (
        <>
            <CustomToast ref={toastRef} />

            <Dialog header={<p className='px-4'>Realizar ajuste de movimiento</p>} visible={visible} style={{ width: '50vw' }} onHide={() => { if (!visible) return; setVisible(false); }}>
                {data ? (
                    <div className='px-4'>
                        <form action="" className='flex flex-col gap-4'>
                            <span>
                                <label htmlFor="">Producto </label>
                                <Dropdown
                                    name="producto"
                                    value={formData?.producto}
                                    onChange={(e) =>
                                        handleChange({ target: { name: 'producto', value: e.value } })
                                    }
                                    options={productosLista}
                                    optionLabel="descripcion"
                                    optionValue="id"
                                    placeholder="Seleccionar producto"
                                    className="md:w-14rem w-full text-start"
                                />
                            </span>
                            <span>
                                <label htmlFor="">Almacen </label>
                                <Dropdown
                                    name="almacen"
                                    value={formData?.almacen}
                                    onChange={(e) =>
                                        handleChange({ target: { name: 'almacen', value: e.value } })
                                    }
                                    options={almacenLista}
                                    optionLabel="nombre"
                                    optionValue="id"
                                    placeholder="Seleccionar almacen"
                                    className="md:w-14rem w-full text-start"
                                />
                            </span>
                            <span>
                                <label htmlFor="">Cantidad ajuste </label>
                                <Input type="number" name="cantidad_ajustada" value={formData.cantidad_ajustada.toString()} onChange={handleChange} />
                            </span>

                            <span>
                                <label htmlFor="">Motivo del ajuste </label>
                                <Input name="motivo" value={formData.motivo} onChange={handleChange} />
                            </span>

                            <span className='flex flex-col'>
                                <label htmlFor="">Fecha </label>
                                <Calendar
                                    name="fecha"
                                    value={formData?.fecha ? dayjs(formData.fecha).toDate() : null} // Convierte la fecha de `formData` a un objeto Date
                                    onChange={handleChange}
                                    dateFormat="dd-mm-yy"  // Formato que quieres mostrar
                                    showIcon
                                    showTime
                                    icon={<CiCalendar size={20} color="rgba(0,0,0,0.5)" />}
                                    iconPos="left"
                                    disabled
                                />
                            </span>
                            <span>
                                <label htmlFor="">Usuario </label>
                                <Input name="usuario" value={formData.usuario} onChange={handleChange} />
                            </span>

                        </form>
                        <span>
                            <button className=' mt-5 border border-primary-blue text-primary-blue px-5 py-2 rounded-md' onClick={saveAjuste}>Realizar ajuste</button>
                        </span>
                    </div>
                ) : (
                    <p>Cargando información del movimiento...</p>
                )}
            </Dialog>
        </>
    )
}
