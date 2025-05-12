import React, { useRef, useState } from 'react';
import { useParams } from 'react-router';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../../shared/toast/customToast';
import { Calendar } from 'primereact/calendar';
import { CiCalendar } from 'react-icons/ci';
import dayjs from 'dayjs';
import { Input } from '../../../../../shared/forms/input';
import { RadioButton } from 'primereact/radiobutton';
import { TablaProveedorSelect } from '../../../../../shared/tablas/tablaProveedorSelect';

interface SteppCrearCompraProps {
  formData: any;
  handleChange: any;
  errorCompra: any;
}

export const SteppCrearCompra: React.FC<SteppCrearCompraProps> = ({
  formData,
  handleChange,
  errorCompra,
}) => {
  const [selectedProveedores, setSelectedProveedores] = useState<any>();
  const [visible, setVisible] = useState(false);
  let params = useParams();
  const toastRef = useRef<CustomToastRef>(null);

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

  return (
    <>
      <CustomToast ref={toastRef} />
      <div>
        <form action="" className="flex flex-col gap-6 text-start">
          <span className="flex flex-col gap-4">
            <span className="flex flex-col gap-2">
              <label htmlFor="">Proveedor</label>
              {selectedProveedores && (
                <Input
                  name="proveedor"
                  value={`${selectedProveedores.nombre} - ${selectedProveedores.id}`}
                  onChange={(e) => {}}
                  disable
                  placeholder="Selecionar proveedor"
                ></Input>
              )}

              <button
                type="button" // evita el submit
                onClick={() => setVisible(true)}
                className="bg-primary-blue self-start rounded-md px-5 py-3 text-white"
              >
                Seleccionar Proveedor
              </button>
            </span>
            <TablaProveedorSelect
              setVisible={setVisible}
              visible={visible}
              setSelectedProveedores={setSelectedProveedores}
              selectedProveedores={selectedProveedores}
              handleChange={handleChange}
            />
            {errorCompra.proveedor && (
              <span className="text-sm text-red-500">
                {errorCompra.proveedor}
              </span>
            )}
          </span>
          <span className="flex flex-col text-start">
            <label htmlFor="">Fecha</label>
            <Calendar
              disabled
              name="fecha"
              value={formData?.fecha ? dayjs(formData.fecha).toDate() : null} // Convertimos el valor a un objeto Date
              onChange={handleChange}
              dateFormat="dd-mm-yy" // Formato de fecha que desees
              showIcon
              showTime
              icon={<CiCalendar size={20} color="rgba(0,0,0,0.5)" />}
              iconPos="left"
              className="bg-gray-200"
            />
          </span>
          <span>
            <label htmlFor="">Total</label>
            <div className="p-inputgroup flex-1">
              <span className="p-inputgroup-addon bg-gray-700 text-white">
                $
              </span>
              <Input
                type="number"
                name="total"
                value={(formData.total ?? 0).toString()}
                onChange={handleChange}
                disable
              />
            </div>
          </span>
          <span className="flex w-full flex-col text-start">
            <label htmlFor="">Estado</label>
            <div className="flex gap-5">
              <div className="align-items-center flex">
                <RadioButton
                  inputId="Pagado"
                  name="estado"
                  value="Pagado"
                  onChange={handleChange}
                  checked={formData?.estado === 'Pagado'}
                />
                <label htmlFor="salida" className="ml-2">
                  Pagado
                </label>
              </div>
              <div className="align-items-center flex">
                <RadioButton
                  inputId="Pendiente"
                  name="estado"
                  value="Pendiente"
                  onChange={handleChange}
                  checked={formData?.estado === 'Pendiente'}
                />
                <label htmlFor="entrada" className="ml-2">
                  Pendiente
                </label>
              </div>
              <div className="align-items-center flex">
                <RadioButton
                  inputId="Cancelado"
                  name="estado"
                  value="Cancelado"
                  onChange={handleChange}
                  checked={formData?.estado === 'Cancelado'}
                />
                <label htmlFor="salida" className="ml-2">
                  Cancelado
                </label>
              </div>
            </div>
            {errorCompra.estado && (
              <span className="text-sm text-red-500">{errorCompra.estado}</span>
            )}
          </span>
          <span>
            <label htmlFor="">Numero documento</label>
            <Input
              name="numero_documento"
              value={formData.numero_documento}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="">Tipo operación</label>
            <Input
              name="tipo_operacion"
              value={formData.tipo_operacion}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="">clasificacion</label>
            <Input
              name="clasificacion"
              value={formData.clasificacion}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="">Sector</label>
            <Input
              name="sector"
              value={formData.sector}
              onChange={handleChange}
            />
          </span>
          <span>
            <label htmlFor="">Tipo de gasto</label>
            <Input
              name="tipo_costo_gasto"
              value={formData.tipo_costo_gasto}
              onChange={handleChange}
            />
          </span>
        </form>
      </div>
    </>
  );
};
