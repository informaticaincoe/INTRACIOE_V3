import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import React, { useState } from 'react';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { FaCheckCircle } from 'react-icons/fa';
import { ModalEliminarItemDeLista } from '../Shared/modal/modalEliminarItemDeLista';
import { ProductosTabla } from '../FE/productosAgregados/productosData';

export const TablaProductosCreditoFiscal = ({}) => {
  const [products, setProducts] = useState<ProductosTabla[]>();
  const [rowClick, setRowClick] = useState<boolean>(true);
  const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
  const [visibleDeleteModal, setVisibleDeleteModal] = useState<boolean>(false);
  const [visibleTributoModal, setVisibleTributoModal] =
    useState<boolean>(false);
  const [visibleRetencionModal, setVisibleRetencionModal] =
    useState<boolean>(false);

  // Función para manejar cambios en la cantidad de un producto específico
  const handleCantidadChange = (value: number | null, productId: number) => {
    setProducts((prevProducts) =>
      prevProducts.map((product) =>
        product.id === productId
          ? { ...product, cantidad: value ?? 0 }
          : product
      )
    );
  };

  // Función para manejar cambios en el descuento de un producto específico
  const handleDescuentoChange = (value: number | null, productId: number) => {
    setProducts((prevProducts) =>
      prevProducts.map((product) =>
        product.id === productId
          ? { ...product, descuento: value ?? 0 }
          : product
      )
    );
  };

  const handleDelete = () => {
    console.log(selectedProducts);
    setVisibleDeleteModal(true);
  };

  const handleRetencion = () => {
    console.log(selectedProducts);
    setVisibleRetencionModal(true);
  };

  return (
    <>
      {selectedProducts.length > 0 && ( // Verificar si hay productos seleccionados
        <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
          <p className="text-blue flex items-center gap-2">
            <FaCheckCircle className="" />
            productos seleccionados {selectedProducts.length}
          </p>
          <span className="flex gap-2">
            <button
              className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
              onClick={handleDelete}
            >
              <p className="text-red">Eliminar</p>
            </button>
            <span className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer">
              <p className="text-blue">Agregar tributo</p>
            </span>
            <span
              className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
              onClick={handleRetencion}
            >
              <p className="text-blue">Agregar retención</p>
            </span>
          </span>
        </div>
      )}
      <ModalEliminarItemDeLista
        setVisible={setVisibleDeleteModal}
        visible={visibleDeleteModal}
        size={selectedProducts.length}
      />
      <ModalAgregarRetencion
        setVisible={setVisibleRetencionModal}
        visible={visibleRetencionModal}
      />

      <DataTable
        value={products}
        tableStyle={{ minWidth: '50rem' }}
        paginator
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
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
        <Column
          field="descripcion"
          header={<p className="text-sm">PRODUCTO</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
          header={<p className="text-sm">PRECIO UNITARIO</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.iva_unitario}</p>}
          header={<p className="text-sm">IVA UNITARIO</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.iva_percibido}</p>}
          header={<p className="text-sm">IVA PERCIBIDO</p>}
        ></Column>
        <Column
          header={<p className="text-sm">CANTIDAD</p>}
          body={(rowData: Product) => (
            <InputNumber
              inputId="withoutgrouping"
              value={rowData.cantidad}
              onValueChange={(e: InputNumberValueChangeEvent) =>
                handleCantidadChange(e.value ?? 0, rowData.id)
              }
            />
          )}
        />
        <Column
          header={<p className="text-sm">DESCUENTO(%)</p>}
          body={(rowData: Product) => (
            <InputNumber
              prefix="%"
              inputId="withoutgrouping"
              value={rowData.descuento}
              onValueChange={(e: InputNumberValueChangeEvent) =>
                handleDescuentoChange(e.value ?? 0, rowData.id)
              }
            />
          )}
        />
        <Column
          body={(rowData: Product) => <p>$ {rowData.total_neto}</p>}
          header={<p className="text-sm">TOTAL NETO</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.total_iva}</p>}
          header={<p className="text-sm">TOTAL IVA</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.total_con_iva}</p>}
          header={<p className="text-sm">TOTAL CON IVA</p>}
        ></Column>
      </DataTable>
    </>
  );
};
