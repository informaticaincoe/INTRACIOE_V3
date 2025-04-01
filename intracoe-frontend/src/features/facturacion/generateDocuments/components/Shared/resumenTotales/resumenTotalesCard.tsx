import React, { useEffect, useState } from 'react';
import { ProductosTabla } from '../../FE/productosAgregados/productosData';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';

interface ResumenTotalesCardProps {
  listProducts: ProductosTabla[];
  setDescuentoGeneral: any;
  descuentoGeneral: number;
  setTotalAPagar:any;
  totalAPagar:number
}

export const ResumenTotalesCard: React.FC<ResumenTotalesCardProps> = ({
  listProducts,
  setDescuentoGeneral,
  descuentoGeneral,
  setTotalAPagar,
  totalAPagar
}) => {
  const [subtotalNeto, setSubtotalNeto] = useState('0.00');
  const [totalIVA, setTotalIVA] = useState('0.00');
  const [descuentoTotal, setDescuentoTotal] = useState('0.00');

  useEffect(() => {
    let neto = 0;
    let iva = 0;
    let descuento = 0;
  
    listProducts.forEach((item) => {
      neto += item.cantidad * item.precio_unitario;
      iva += item.cantidad * item.iva_unitario;
      if (item.descuento && typeof item.descuento.porcentaje === 'number') {
        descuento += item.cantidad * item.precio_unitario * item.descuento.porcentaje;
      }
    });
  
    setSubtotalNeto(neto.toFixed(2));
    setTotalIVA(iva.toFixed(2));
    setDescuentoTotal(descuento.toFixed(2));
    // Actualiza totalAPagar
    setTotalAPagar((neto + iva - descuento).toFixed(2));
  }, [listProducts, setTotalAPagar]); // Se asegura de que se actualice cuando listProducts cambie
  

  return (
    <div className="grid grid-cols-[auto_1fr_auto_1fr] gap-4 text-start">
      <p className="opacity-60">SubTotal Neto:</p>
      <p>$ {subtotalNeto}</p>

      <p className="opacity-60">Total IVA:</p>
      <p>$ {totalIVA}</p>

      <p className="opacity-60">Total con IVA:</p>
      <p>$ {(totalAPagar)}</p>

      <p className="opacity-60">Monto descuento:</p>
      <p>$ {descuentoTotal}</p>

      <p className="opacity-60">Total a pagar:</p>
      <p>$ {totalAPagar}</p>

      <p className="opacity-60">Descuento general:</p>
      <InputNumber
        prefix="%"
        value={descuentoGeneral}
        onValueChange={(e: InputNumberValueChangeEvent) =>
          setDescuentoGeneral(e.value ?? 0)
        }
        style={{ padding: 0, height: '2rem' }}
      />
    </div>
  );
};
