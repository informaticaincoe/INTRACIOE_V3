import React, { useEffect } from 'react'
import { ProductosTabla } from '../../FE/productosAgregados/productosData'
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber'

interface ResumenTotalesCardProps {
    listProducts: ProductosTabla[],
    setDescuentoGeneral: any,
    descuentoGeneral: number
}

export const ResumenTotalesCard: React.FC<ResumenTotalesCardProps> = ({ listProducts, setDescuentoGeneral, descuentoGeneral }) => {

    useEffect(() => {
        console.log("descuento", listProducts)
    }, [])

    const CalcularTotalIVA = () => {
        let aux = 0;
        listProducts.forEach((item) => {
            aux += item.cantidad * item.iva_unitario
        })

        return aux
    }

    const CalcularTotalNeto = () => {
        let aux = 0
        listProducts.forEach((item) => {
            aux += item.cantidad * item.precio_unitario
        })
        return aux
    }

    const CalcularDescuento = () => {
        let aux = 0
        listProducts.forEach((item) => {
            aux += item.cantidad * (item.precio_unitario * (item.descuento / 100))
        })
        return aux
    }

    const CalcularTotalConIVA = () => {
        let aux = 0
        aux += CalcularTotalNeto() + CalcularTotalIVA() 
        
        return aux
    }

    return (
        <div className="grid grid-cols-[auto_1fr_auto_1fr] gap-4 text-start">
            <p className="opacity-60">SubTotal Neto:</p>
            <p>${CalcularTotalNeto()}</p>

            <p className="opacity-60">Total IVA:</p>
            <p>${CalcularTotalIVA()}</p>

            <p className="opacity-60">Total con IVA:</p>
            <p>${CalcularTotalConIVA()}</p>

            <p className="opacity-60">Monto descuento:</p>
            <p>$ {CalcularDescuento()}</p>

            <p className='opacity-60'>Total a pagar:</p>
            <p>{CalcularTotalConIVA()}</p>

            <p className='opacity-60'>Descuento general:</p>
            <InputNumber
                prefix="%"
                value={descuentoGeneral}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                    setDescuentoGeneral(e.value ?? 0)
                }
                style={{ padding: 0, height: '2rem' }}
            />
        </div>
    )
}
