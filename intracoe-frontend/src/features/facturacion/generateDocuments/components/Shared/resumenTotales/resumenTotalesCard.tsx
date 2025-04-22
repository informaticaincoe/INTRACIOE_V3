import React, { useEffect, useState } from 'react';
import { ProductosTabla } from '../../FE/productosAgregados/productosData';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { Descuentos } from '../../../../../../shared/interfaces/interfaces';

interface ResumenTotalesCardProps {
  listProducts: ProductosTabla[];
  descuentos: Descuentos;
  setDescuentos: React.Dispatch<React.SetStateAction<Descuentos>>;
  setTotalAPagar: any;
  totalAPagar: number;
  tipoDocumento: string;
}

export const ResumenTotalesCard: React.FC<ResumenTotalesCardProps> = ({
  listProducts,
  setDescuentos,
  descuentos,
  setTotalAPagar,
  totalAPagar,
  tipoDocumento,
}) => {
  const [subtotalNeto, setSubtotalNeto] = useState('0.00');
  const [totalIVA, setTotalIVA] = useState('0.00');
  const [totalConIva, setTotalConIva] = useState('0.00');
  const [descuentoTotal, setDescuentoTotal] = useState('0.00');

  useEffect(() => {
    console.log('ListProducts', listProducts);
    console.log('Descuentos', descuentos);
    console.log('Total a pagar', totalAPagar);
  }, [listProducts, descuentos, totalAPagar]);

  useEffect(() => {
    // 1) Suma de importes base
    let neto = 0; // base gravada (sin IVA)
    let iva = 0; // IVA de cada ítem
    let totalConIvaAux = 0; // precio bruto (con IVA)
    let descuentosItem = 0;

    listProducts.forEach((item) => {
      neto += item.total_neto;
      iva += item.total_iva;
      totalConIvaAux += item.total_con_iva;
      descuentosItem += item.descuento?.porcentaje ?? 0;
    });

    // 2) Calcula descuentos
    const descGravadoAmount = neto * (descuentos.descuentoGravado / 100);
    const descGeneralAmount =
      totalConIvaAux * (descuentos.descuentoGeneral / 100);
    const totalDescuento = descGravadoAmount + descGeneralAmount;

    // 3) Aplica descuentos
    const totalAfterDesc = totalConIvaAux - totalDescuento;

    // 4) Actualiza estados
    setSubtotalNeto(neto.toFixed(2));
    setTotalIVA(iva.toFixed(2));

    // Si el documento lleva IVA (por ej. tipo "01"), muestra total con IVA descontado
    if (tipoDocumento === '01') {
      setTotalConIva(totalAfterDesc.toFixed(2));
    } else {
      // si no lleva IVA, el total es neto menos descuentos
      setTotalConIva((neto - totalDescuento).toFixed(2));
    }

    setDescuentoTotal(descuentosItem.toFixed(2));

    // 5) Notifica al padre el nuevo total a pagar (número, no string)
    setTotalAPagar(Number(totalAfterDesc.toFixed(2)));
  }, [listProducts, descuentos, tipoDocumento]);

  return (
    <div className="grid grid-cols-[auto_1fr_auto_1fr] gap-4 text-start">
      <p className="opacity-60">SubTotal Neto:</p>
      <p>$ {subtotalNeto}</p>

      <p className="opacity-60">Total con IVA:</p>
      <p>$ {totalConIva}</p>

      <p className="opacity-60">Monto descuento:</p>
      <p>$ {descuentoTotal}</p>

      <p className="opacity-60">Total IVA:</p>
      <p>$ {totalIVA}</p>

      <p className="opacity-60">Total a pagar:</p>
      <p>$ {totalAPagar.toFixed(2)}</p>

      <p className="opacity-60">Descuento general:</p>
      <InputNumber
        prefix="%"
        value={descuentos.descuentoGeneral}
        onValueChange={(e: InputNumberValueChangeEvent) =>
          setDescuentos((prev: any) => ({
            ...prev,
            descuentoGeneral: e.value ?? 0,
          }))
        }
        style={{ padding: 0, height: '2rem' }}
      />
      <p></p>
      <p></p>
      <p className="opacity-60">Descuento Ventas grabadas:</p>
      <InputNumber
        prefix="%"
        value={descuentos.descuentoGravado}
        onValueChange={(e: InputNumberValueChangeEvent) =>
          setDescuentos((prev: any) => ({
            ...prev,
            descuentoGravado: e.value ?? 0,
          }))
        }
        style={{ padding: 0, height: '2rem' }}
      />
    </div>
  );
};
