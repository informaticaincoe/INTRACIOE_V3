import React, { useEffect, useRef, useState } from 'react';
import { compraResult, DetalleCompraInterfaz } from '../../compras/interfaces/comprasInterfaces';
import { Dialog } from 'primereact/dialog';
import { RadioButton } from 'primereact/radiobutton';
import { InputTextarea } from 'primereact/inputtextarea';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Input } from '../../../../shared/forms/input';
import { createDevolucionesCompra } from '../services/devolucionesCompraServices';
import { useNavigate } from 'react-router';
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast';
import { IoMdCloseCircle } from 'react-icons/io';
import { FaCheckCircle } from 'react-icons/fa';

interface ModalDetallesCompraProp {
  data: compraResult;
  visible: boolean;
  setVisible: (v: boolean) => void;
  productos: DetalleCompraInterfaz[];
}

export const ModalDevolucionCompra: React.FC<ModalDetallesCompraProp> = ({
  data,
  visible,
  setVisible,
  productos
}) => {
  const toastRef = useRef<CustomToastRef>(null);
  const [formDataProductos, setFormDataProductos] = useState<any[]>([]);
  const [estado, setEstado] = useState<string>('');
  const [motivo, setMotivo] = useState<string>('');
  const navigate = useNavigate()

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

  // 1) Inicializar con codigo, descripción y cantidad original
  useEffect(() => {
    const list: any[] = productos.map(p => ({
      id: p.producto,
      codigo: p.codigo,
      descripcion: p.descripcion,
      cantidad: p.cantidad,
      motivo: ''
    }));
    setFormDataProductos(list);
  }, [productos]);

  // 2) Handler genérico para actualizar sólo un campo de una fila
  const handleChangeCompraProductos = (
    rowIndex: number,
    field: keyof any,
    value: string | number
  ) => {
    setFormDataProductos(prev => {
      const copy = [...prev];
      copy[rowIndex] = { ...copy[rowIndex], [field]: value };
      return copy;
    });
  };

  // 3) Enviar payload
  const handleRealizarDevolucion = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      compra: data.id,
      detalles: formDataProductos.map(d => ({
        producto: d.id,
        cantidad: d.cantidad,
        motivo_detalle: d.motivo
      })),
      motivo,
      estado,
      usuario: 'admin'
    };

    console.log(JSON.stringify(payload, null, 2));

    try {
      await createDevolucionesCompra(payload)
      handleAccion('success', <FaCheckCircle />, 'Devolución creada con exíto');

      setTimeout(() => {
        navigate("/devoluciones-compra/")
      }, 2000);
    } catch (error) {
      console.log(error)
      handleAccion('error', <IoMdCloseCircle />, 'Error al realizar devolución');

    }
  };

  return (
    <>
      <CustomToast ref={toastRef} />

      <Dialog
        header="Realizar devolución"
        visible={visible}
        onHide={() => setVisible(false)}
        style={{ width: '40vw' }}
        breakpoints={{ '1679px': '60vw', '1462px': '60vw' }}
      >
        <form className="flex flex-col gap-6" onSubmit={handleRealizarDevolucion}>
          <label className="font-semibold">Productos</label>

          {/* 4) Usar formDataProductos */}
          <DataTable value={formDataProductos} tableStyle={{ minWidth: '100%' }}>
            <Column field="codigo" header="Código" />
            <Column field="descripcion" header="Producto" />

            <Column header="Cantidad" body={(rowData, { rowIndex }) => (
              <Input
                name='cantidad'
                type="number"
                value={rowData.cantidad}
                onChange={e =>
                  handleChangeCompraProductos(
                    rowIndex,
                    'cantidad',
                    Number(e.target.value)
                  )
                }
                className="w-24"
                minNum={0}
              />
            )} />

            <Column header="Motivo" body={(rowData, { rowIndex }) => (
              <Input
                name='motivo'
                value={rowData.motivo}
                onChange={e =>
                  handleChangeCompraProductos(
                    rowIndex,
                    'motivo',
                    e.target.value
                  )
                }
                className="w-full"
              />
            )} />
          </DataTable>

          <label className="font-semibold">Motivo general</label>
          <InputTextarea
            value={motivo}
            onChange={e => setMotivo(e.target.value)}
            rows={4}
            className="w-full"
          />

          <label className="font-semibold">Estado</label>
          <div className="flex gap-6">
            {['Aprobada', 'Pendiente', 'Rechazada'].map(val => (
              <div key={val} className="flex items-center gap-2">
                <RadioButton
                  inputId={val}
                  name="estado"
                  value={val}
                  onChange={e => setEstado(e.value)}
                  checked={estado === val}
                />
                <label htmlFor={val}>{val}</label>
              </div>
            ))}
          </div>

          <div className="mt-6 flex justify-end gap-4">
            <button
              type="button"
              onClick={() => setVisible(false)}
              className="px-4 py-2 border rounded"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-primary-blue text-white rounded"
            >
              Realizar devolución
            </button>
          </div>
        </form>
      </Dialog>
    </>
  );
};
