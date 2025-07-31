import { useEffect, useState } from 'react';

interface ResumenCardNotaAjusteInterface {
  facturas?: any[];
  cantidades: any;
  totalAPagar: number;
}

export const ResumenCardNotaAjuste: React.FC<
  ResumenCardNotaAjusteInterface
> = ({ facturas, cantidades, totalAPagar }) => {
  const [subtotalNeto, setSubtotalNeto] = useState<number>(0);
  const [descuento, setDescuento] = useState<number>(0);
  const [totalIva, setTotalIva] = useState<number>(0);
  const [totalConIva, setTotalConIva] = useState<number>(0);
  const [saldoFavor, setSaldoFavor] = useState<number>(0);

  useEffect(() => {
    if (facturas) {
      console.log(cantidades)
      const subtotalNetoAux = facturas.reduce(
        (sum, r, index) => sum + (((r.preunitario) * cantidades[index])),
        0
      );
      setSubtotalNeto(subtotalNetoAux);

      const descuentoAux = facturas.reduce(
        (sum, r) => sum + (r.descuento ?? 0),
        0
      );
      setDescuento(descuentoAux);

      const totalIvaAux = facturas.reduce(
        (sum, r, index) => sum + (r.iva_unitario * cantidades[index]),
        0
      );
      setTotalIva(totalIvaAux.toFixed(2));

      const totalConIvaAux = facturas.reduce(
        (sum, r, index) => sum + (Math.round(((parseFloat(r.iva_unitario) + parseFloat(r.preunitario)) * parseFloat(cantidades[index]))*100)/100),
        0
      );
      setTotalConIva(totalConIvaAux);

      console.log("TIPO", typeof(totalConIvaAux))

      const saldoFavorAux = facturas.reduce(
        (sum, r) => sum + (r.saldo_a_favor ?? 0),
        0
      );
      setSaldoFavor(saldoFavorAux);
    }
  }, [facturas]);

  return (
    <div className="grid grid-cols-[auto_1fr_auto_1fr] gap-4 text-start">
      <p className="opacity-60">SubTotal Neto:</p>
      <p>$ {subtotalNeto}</p>

      <p className="opacity-60">Descuento</p>
      <p>$ {descuento}</p>

      <p className="opacity-60">Total IVA:</p>
      <p>$ {totalIva}</p>

      <p className="opacity-60">Saldo a favor:</p>
      <p>$ {saldoFavor}</p>

      <p className="opacity-60">Total con IVA:</p>
      <p>$ {totalConIva}</p>

      <p></p>
      <p></p>

      <p className="opacity-60">Total a Pagar:</p>
      <p>$ {totalAPagar.toFixed(2)}</p>

      {/*
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

            <p className="opacity-60">Monto descuento:</p>
            <p>$ {descuentoTotal}</p>

            <p className="opacity-60">Saldo a favor:</p>
            <InputNumber
                prefix="$"
                value={saldoFavor}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                    setSaldoFavor(e.value)
                }
                style={{ padding: 0, height: '2rem' }}
            />

           

            <p></p>
            <p></p>

            <p className="opacity-60">Total a pagar:</p>
            <p>$ {totalAPagar.toFixed(2)}</p>


 */}
    </div>
  );
};
