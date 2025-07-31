import React, { useRef, useState } from 'react';
import { CustomToastRef } from '../../../../../shared/toast/customToast';
import { ModalDetallesProductos } from './modalDetallesProductos';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { DetalleCompraPayload } from '../../interfaces/comprasInterfaces';
import { ColumnGroup } from 'primereact/columngroup';
import { Row } from 'primereact/row';
import { FaPlus } from 'react-icons/fa6';
import { FaCheckCircle } from 'react-icons/fa';

interface SteppDetallesProductoProps {
  detalles: any;
  setDetalles: any;
}

export const SteppListaProducto: React.FC<SteppDetallesProductoProps> = ({
  detalles,
  setDetalles,
}) => {
  const toastRef = useRef<CustomToastRef>(null);
  const [visible, setVisible] = useState(false);
  const [rowClick] = useState<boolean>(true);
  const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
  const [detalleToEdit, setDetalleToEdit] =
    useState<DetalleCompraPayload | null>(null);

  const handleAddDetalle = (detalle: DetalleCompraPayload) => {
    setDetalles((prev: any) => [...prev, detalle]);
    toastRef.current?.show({
      severity: 'success',
      summary: 'Detalle agregado',
      life: 2000,
    });
  };

  const handleDelete = () => {
    const selectedIds = selectedProducts.map((product) => product.id);
    const nuevosDetalles = detalles.filter(
      (detalle: any) => !selectedIds.includes(detalle.id)
    );
    setDetalles(nuevosDetalles);
    setSelectedProducts([]); // Limpia la selección
    toastRef.current?.show({
      severity: 'warn',
      summary: 'Productos eliminados',
      life: 2000,
    });
  };

  const handleEdit = () => {
    if (selectedProducts.length === 1) {
      setDetalleToEdit(selectedProducts[0]);
      setVisible(true);
    }
  };

  const footerGroup = (
    <ColumnGroup>
      <Row>
        <Column
          footer={
            <button
              type="button"
              onClick={() => setVisible(true)}
              className="flex items-center gap-2 rounded border border-blue-600 px-4 py-2 text-blue-600"
            >
              <FaPlus />
              Agregar producto
            </button>
          }
          colSpan={5}
        />
      </Row>
    </ColumnGroup>
  );

  const handleUpdateDetalle = (detalleEditado: DetalleCompraPayload) => {
    const nuevosDetalles = detalles.map((d: DetalleCompraPayload) =>
      d.id === detalleEditado.id ? detalleEditado : d
    );
    setDetalles(nuevosDetalles);
    setSelectedProducts([]);
    toastRef.current?.show({
      severity: 'info',
      summary: 'Producto actualizado',
      life: 2000,
    });
  };

  return (
    <>
      {/* <CustomToast ref={toastRef} /> */}
      {selectedProducts.length > 0 && ( // Verificar si hay productos seleccionados
        <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
          <p className="text-blue flex items-center gap-2">
            <FaCheckCircle className="" />
            productos seleccionados {selectedProducts.length}
          </p>
          <span className="flex gap-2">
            {selectedProducts.length === 1 && (
              <span
                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={handleEdit}
              >
                <p className="text-blue">Editar</p>
              </span>
            )}
            {
              <button
                className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={handleDelete}
              >
                <p className="text-red">Eliminar</p>
              </button>
            }
          </span>
        </div>
      )}
      <DataTable
        value={detalles}
        className="mt-4"
        tableStyle={{ minWidth: '100%' }}
        footerColumnGroup={footerGroup}
        selectionMode={rowClick ? null : 'multiple'}
        selection={selectedProducts!}
        onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
          setSelectedProducts(e.value)
        }
      >
        <Column
          selectionMode="multiple"
          headerStyle={{ width: '3rem' }}
        ></Column>
        <Column field="codigo" header="Código" />
        <Column field="descripcion" header="Descripción" />
        <Column field="cantidad" header="Cant." />
        <Column field="precio_unitario" header="Precio U." />
        <Column field="precio_venta" header="Precio V." />
      </DataTable>

      <ModalDetallesProductos
        visible={visible}
        setVisible={(v) => {
          setVisible(v);
          if (!v) setDetalleToEdit(null); // Limpiar después de cerrar
        }}
        onAdd={handleAddDetalle}
        onUpdate={handleUpdateDetalle}
        detalleToEdit={detalleToEdit}
      />
    </>
  );
};
