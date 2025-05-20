import React, { useEffect, useState } from 'react';
import { ProductosTabla } from '../../FE/productosAgregados/productosData';
import {
    InputNumber,
    InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { Descuentos } from '../../../../../../shared/interfaces/interfaces';

interface TablaTotalesSujetoExcluidoProps {
    selectedProducts:any
    cantidadListProducts:any[],
    idListProducts:any[]
    descuentoGeneral: number,
    setDescuentoGeneral:any,
    setTotalAPagar:any
    totalAPagar:any 
}

export const TablaTotalesSujetoExcluido: React.FC<TablaTotalesSujetoExcluidoProps> = ({
    selectedProducts,
    cantidadListProducts,
    idListProducts,
    descuentoGeneral,
    setTotalAPagar,
    setDescuentoGeneral,
    totalAPagar
}) => {
    const [subtotalNeto, setSubtotalNeto] = useState('0.00');
    const [totalIVA, setTotalIVA] = useState('0.00');
    const [totalConIva, setTotalConIva] = useState('0.00');
    const [descuentoTotal, setDescuentoTotal] = useState('0.00');

    useEffect(() => {
       
    }, [selectedProducts, descuentoGeneral, cantidadListProducts]);

    return (
        <div className="grid grid-cols-[auto_1fr_auto_1fr] gap-4 text-start">
            <p className="opacity-60">SubTotal Neto:</p>
            <p>$ {subtotalNeto}</p>

            <p className="opacity-60">Descuento general:</p>
            <InputNumber
                prefix="%"
                value={descuentoGeneral}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                    setDescuentoGeneral((prev: any) => ({
                        ...prev,
                        descuentoGeneral: e.value ?? 0,
                    }))
                }
                style={{ padding: 0, height: '2rem' }}
            />

            <p className="opacity-60">Total con IVA:</p>
            <p>$ {totalConIva}</p>

            <p className="opacity-60">Monto descuento:</p>
            <p>$ {descuentoTotal}</p>

            <p></p>
            <p></p>

            <p className="opacity-60">Total IVA:</p>
            <p>$ {totalIVA}</p>

            <p></p>
            <p></p>

            <p className="opacity-60">Total a pagar:</p>
            <p>$ {totalAPagar.toFixed(2)}</p>

        </div>
    );
};
