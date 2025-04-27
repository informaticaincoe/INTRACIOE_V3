import { useEffect } from 'react';
import { Checkbox } from 'primereact/checkbox';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';

interface CheckBoxRetencionProps {
  setTieneRetencionIva: any;
  tieneRetencionIva: boolean;
  setRetencionIva: any;
  retencionIva: number;
  setTieneRetencionRenta: any;
  tieneRetencionRenta: boolean;
  retencionRenta: number;
  setRetencionRenta: any;
}
export const CheckBoxRetencion: React.FC<CheckBoxRetencionProps> = ({
  setTieneRetencionIva,
  tieneRetencionIva,
  setRetencionIva,
  retencionIva,
  setTieneRetencionRenta,
  tieneRetencionRenta,
  retencionRenta,
  setRetencionRenta,
}) => {
  let total = 0;

  useEffect(() => {
    calcularTotalRetencion();
  }, [tieneRetencionIva, tieneRetencionRenta]);

  const calcularTotalRetencion = () => {
    if (tieneRetencionIva) total = total + retencionIva;
    if (tieneRetencionRenta) total = total + retencionRenta;

    return total;
  };

  const handleRetencionRenta = (value: boolean) => {
    setTieneRetencionRenta(value);
  };

  const handleRetencionIVA = (value: boolean) => {
    setTieneRetencionIva(value);
  };

  return (
    <>
      <div className="flex gap-3 text-start">
        <Checkbox
          inputId="renta"
          onChange={(e) => handleRetencionRenta(e.checked ?? false)}
          checked={tieneRetencionRenta}
        ></Checkbox>
        <label htmlFor="renta" className="opacity-70">
          Retención de renta
        </label>
      </div>
      {tieneRetencionRenta && (
        <InputNumber
          prefix="%"
          inputId="withoutgrouping"
          value={retencionRenta}
          onValueChange={(e: InputNumberValueChangeEvent) =>
            setRetencionRenta(e.value ?? 0)
          }
          className="w-full"
        />
      )}
      <div className="flex gap-3 text-start">
        <Checkbox
          inputId="iva"
          onChange={(e) => handleRetencionIVA(e.checked ?? false)}
          checked={tieneRetencionIva}
        ></Checkbox>
        <label htmlFor="iva" className="opacity-70">
          Retención de IVA
        </label>
      </div>
      {tieneRetencionIva && (
        <InputNumber
          prefix="%"
          inputId="withoutgrouping"
          value={retencionIva}
          onValueChange={(e: InputNumberValueChangeEvent) =>
            setRetencionIva(e.value ?? 0)
          }
          className="w-full"
        />
      )}
      {(tieneRetencionIva === true || tieneRetencionRenta === true) && (
        <p className="text-start">
          Total retencion: ${calcularTotalRetencion()}
        </p>
      )}
    </>
  );
};
