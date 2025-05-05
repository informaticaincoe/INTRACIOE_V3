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
import { DetalleCompra } from '../../interfaces/comprasInterfaces';
import { ProductoResponse } from '../../../../../shared/interfaces/interfaces';
import { getAllProducts } from '../../../../../shared/services/productos/productosServices';

interface SteppDetallesProductoProps {
    formData: DetalleCompra,
    handleChange: any
}

export const SteppDetallesProducto: React.FC<SteppDetallesProductoProps> = ({ formData, handleChange }) => {
    let params = useParams();
    const toastRef = useRef<CustomToastRef>(null);
    const [productosLista, setProductosLista] = useState<ProductoResponse[]>([])


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
        fetchProducts()
    }, [])


    const fetchProducts = async () => {
        try {
            const response = await getAllProducts()
            setProductosLista(response)
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }
    return (
        <>
            <form action="" className='text-start flex flex-col gap-4'>
                <span className=''>
                    <label htmlFor="">Producto</label>
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
                <span className=''>
                    <label htmlFor="">Cantidad</label>
                    <Input type="number" name="cantidad" value={formData.cantidad.toString()} onChange={handleChange} />
                </span>
                <span className=''>
                    <label htmlFor="">Precio unitario</label>
                    <Input type="number" name="precio_unitario" value={formData.precio_unitario.toString()} onChange={handleChange} />
                </span>
                <span className=''>
                    <label htmlFor="">SubTotal</label>
                    <Input type="number" name="subtotal" value={formData.subtotal.toString()} onChange={handleChange} />
                </span>

            </form>
        </>
    )
}
