import { useEffect, useState } from "react";
import { Checkbox } from "primereact/checkbox";
import { InputNumber, InputNumberValueChangeEvent } from "primereact/inputnumber";

interface CheckBoxRetencionProps {
    setTieneRetencionIva:any,
    tieneRetencionIva:boolean,
    setRetencionIva:any
    retencionIva:number,

}
export const CheckBoxRetencion:React.FC<CheckBoxRetencionProps> = ({setTieneRetencionIva, tieneRetencionIva, setRetencionIva, retencionIva }) => {
    const [checkedRenta, setCheckedRenta] = useState<boolean>(false);
    const [renta, setRenta] = useState<number>(0);

    const [visibleRetencion, setVisibleRetencion] = useState<boolean>(false)
    const [visibleIVA, setVisibleIVA] = useState<boolean>(false)

    let total = 0;

    useEffect(() => {
        calcularTotalRetencion();
    }, [tieneRetencionIva, checkedRenta]);

    const calcularTotalRetencion = () => {
        if (tieneRetencionIva) total = total + retencionIva;
        if (checkedRenta) total = total + renta;

        return (total)
    }

    const handleRetencionRenta = (e: boolean) => {
        setCheckedRenta(e)
        setVisibleRetencion(true);
    };

    const handleRetencionIVA = (e: boolean) => {
        setTieneRetencionIva(e)
        setVisibleIVA(true);
    };

    return (
        <>
            <div className="flex gap-3 text-start">
                <Checkbox
                    inputId="renta"
                    onChange={(e) => handleRetencionRenta(e.checked ?? false)}
                    checked={checkedRenta}
                ></Checkbox>
                <label htmlFor="renta" className="opacity-70">
                    Retención de renta
                </label>
            </div>
            {checkedRenta &&
                <InputNumber
                    prefix="%"
                    inputId="withoutgrouping"
                    value={renta}
                    onValueChange={(e: InputNumberValueChangeEvent) =>
                        setRenta(e.value ?? 0)
                    }
                    className="w-full"
                />
            }
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
            {tieneRetencionIva &&
                <InputNumber
                    prefix="%"
                    inputId="withoutgrouping"
                    value={retencionIva}
                    onValueChange={(e: InputNumberValueChangeEvent) =>
                        setRetencionIva(e.value ?? 0)
                    }
                    className="w-full"
                />
            }
            {(tieneRetencionIva === true || checkedRenta === true) && (
                <p className="text-start">Total retencion: ${calcularTotalRetencion()}</p>
            )}


        </>
    )
}
