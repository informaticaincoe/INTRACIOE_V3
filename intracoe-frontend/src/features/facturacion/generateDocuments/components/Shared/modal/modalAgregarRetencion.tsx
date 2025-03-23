import { Checkbox } from 'primereact/checkbox';
import { Dialog } from 'primereact/dialog';
import { Divider } from 'primereact/divider';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import React, { useEffect, useState } from 'react';

interface ModalEliminarInterface {
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  visible: boolean;
  setVisible: any;
}

export const ModalAgregarRetencion: React.FC<ModalEliminarInterface> = ({
  onClick,
  visible,
  setVisible,
}) => {
  const [checkedIva, setCheckedIva] = useState<boolean>(false);
  const [checkedRenta, setCheckedRenta] = useState<boolean>(false);
  const [iva, setIva] = useState<number>(0);
  const [renta, setRenta] = useState<number>(0);
  let total = 0;

  // const [renta, setRenta] = useState<number>(0)

  useEffect(() => {
    calcularTotalRetencion();
  }, [checkedIva, checkedRenta]);

  const calcularTotalRetencion = () => {
    if (checkedIva) total = total + iva;
    if (checkedRenta) total = total + renta;

    return total;
  };
  return (
    <div className="justify-content-center flex">
      <Dialog
        header="Agregar retención"
        visible={visible}
        style={{ width: '40vw' }}
        onHide={() => {
          if (!visible) return;
          setVisible(false);
        }}
      >
        <div className="flex flex-col gap-5 py-5">
          <div className="flex flex-col gap-2">
            <>
              <span className="flex gap-2">
                <Checkbox
                  inputId="VentaTerceros"
                  onChange={(e) => setCheckedIva(e.checked ?? false)}
                  checked={checkedIva}
                ></Checkbox>
                <label htmlFor="VentaTerceros">IVA</label>
              </span>
            </>
            <>
              <label htmlFor="porcentajeRetencion">
                Porcentaje de retención
              </label>
              <InputNumber
                prefix="%"
                inputId="withoutgrouping"
                value={iva}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                  setIva(e.value ?? 0)
                }
                className="w-full"
                disabled={!checkedIva}
              />
            </>
          </div>

          <div className="flex flex-col gap-2">
            <div className="flex flex-col gap-2">
              <span className="flex gap-2">
                <Checkbox
                  inputId="VentaTerceros"
                  onChange={(e) => setCheckedRenta(e.checked ?? false)}
                  checked={checkedRenta}
                ></Checkbox>
                <label htmlFor="VentaTerceros">Renta</label>
              </span>
            </div>
            <div>
              <label htmlFor="porcentajeRetencion">
                Porcentaje de retención
              </label>
              <InputNumber
                prefix="%"
                inputId="withoutgrouping"
                value={renta}
                onValueChange={(e: InputNumberValueChangeEvent) =>
                  setRenta(e.value ?? 0)
                }
                className="w-full"
                disabled={!checkedRenta}
              />
            </div>
          </div>
        </div>
        <Divider />
        <span className="flex justify-between">
          <p>Total retencion: {calcularTotalRetencion()}%</p>
          <span className="flex justify-end gap-2">
            <button
              className="bg-primary-blue w-[8vw] rounded-md py-2 text-white hover:cursor-pointer"
              onClick={onClick}
            >
              Aplicar
            </button>
            <button
              className="border-grauy text-grauy w-[8vw] rounded-md border py-2 hover:cursor-pointer"
              onClick={() => setVisible(false)}
            >
              Cancelar
            </button>
          </span>
        </span>
      </Dialog>
    </div>
  );
};
