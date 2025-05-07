import React, { useEffect, useRef, useState } from 'react'
import { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast';
import { Input } from '../../../../../shared/forms/input';
import { ProductoResponse, TipoUnidadMedida } from '../../../../../shared/interfaces/interfaces';
import { getAllProducts, getAllUnidadesDeMedida } from '../../../../../shared/services/productos/productosServices';
import { Dropdown } from 'primereact/dropdown';

interface SteppDetallesProductoProps {
    formData: any,
    handleChangeDetalle: any
    errorsDetalle: any
}

export const SteppDetallesProducto: React.FC<SteppDetallesProductoProps> = ({ formData, handleChangeDetalle, errorsDetalle }) => {
    const toastRef = useRef<CustomToastRef>(null);
    const [productosLista, setProductosLista] = useState<ProductoResponse[]>([])
    const [unidadMedida, setUnidadMedida] = useState<TipoUnidadMedida[]>([])

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
        fetchUnidadMedida()
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

    const fetchUnidadMedida = async () => {
        try {
            const response = await getAllUnidadesDeMedida()
            setUnidadMedida(response)
            console.log(response)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <>
            <form action="" className='text-start flex flex-col gap-4'>
                {/* <span className=''>
                    <label htmlFor="">Producto</label>
                    <Dropdown
                        name="producto"
                        value={formData?.producto}
                        onChange={ handleChange({: { name: 'producto', value: e } })
                        }
                        options={productosLista}
                        optionLabel="descripcion"
                        optionValue="id"
                        placeholder="Seleccionar producto"
                        className="md:w-14rem w-full text-start"
                    />
                </span> */}
                <span className=''>
                    <label htmlFor="">Codigo</label>
                    <Input
                        name="codigo"
                        value={formData.codigo}
                        onChange={handleChangeDetalle}
                        className={`${errorsDetalle.codigo ? 'border-red' : 'border-border-color'}`}
                    />
                    {errorsDetalle.codigo && (
                        <span className="text-sm text-red-500">{errorsDetalle.codigo}</span>
                    )}
                </span>
                <span className=''>
                    <label htmlFor="">Descripcion</label>
                    <Input
                        name="descripcion"
                        value={formData.descripcion}
                        onChange={handleChangeDetalle}
                        className={`${errorsDetalle.descripcion ? 'border-red' : 'border-border-color'}`}
                    />
                    {errorsDetalle.descripcion && (
                        <span className="text-sm text-red-500">{errorsDetalle.descripcion}</span>
                    )}
                </span>
                <span className=''>
                    <label htmlFor="">Cantidad</label>
                    <Input
                        type="number"
                        name="cantidad"
                        value={formData.cantidad}
                        onChange={handleChangeDetalle}
                        className={`${errorsDetalle.cantidad ? 'border-red' : 'border-border-color'}`}
                    />
                    {errorsDetalle.descripcion && (
                        <span className="text-sm text-red-500">{errorsDetalle.cantidad}</span>
                    )}
                </span>
                <span className=''>
                    <label htmlFor="">Precio unitario</label>
                    <Input
                        type="number"
                        name="precio_unitario"
                        value={formData.precio_unitario}
                        onChange={handleChangeDetalle}
                        className={`${errorsDetalle.precio_unitario ? 'border-red' : 'border-border-color'}`}
                    />
                    {errorsDetalle.precio_unitario && (
                        <span className="text-sm text-red-500">{errorsDetalle.precio_unitario}</span>
                    )}
                </span>
                <span className=''>
                    <label htmlFor="">Precio venta</label>
                    <Input
                        type="number"
                        name="precio_venta"
                        value={formData.precio_venta}
                        onChange={handleChangeDetalle}
                        className={`${errorsDetalle.precio_venta ? 'border-red' : 'border-border-color'}`}
                    />
                    {errorsDetalle.precio_venta && (
                        <span className="text-sm text-red-500">{errorsDetalle.precio_venta}</span>
                    )}
                </span>
                <span className=''>
                    <label htmlFor="">Unidad de medida</label>
                    <Dropdown
                        name="unidad_medida"
                        value={formData?.unidad_medida}
                        onChange={(e) =>
                            handleChangeDetalle({
                                target: {
                                    name: "unidad_medida",
                                    value: e.value,
                                },
                            })
                        }
                        options={unidadMedida}
                        optionLabel="descripcion"
                        optionValue="id"
                        placeholder="Seleccionar unidad"
                        className={`md:w-14rem w-full text-start `}
                    />
                </span>
            </form>
        </>
    )
}
