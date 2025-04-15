import React, { useEffect, useRef, useState } from 'react';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Image } from 'primereact/image';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';

import { deleteProduct } from '../services/productsServices';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate } from 'react-router';

export interface TablaProductosProps {
  productos: ProductoResponse[];
  refreshProducts: () => void;
}

export const TablaProductos: React.FC<TablaProductosProps> = ({
  productos,
  refreshProducts,
}) => {
  useEffect(() => {
    console.log(productos);
  }, [productos]);

  const [rowClick] = useState<boolean>(true);
  const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

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

  const handleDelete = async () => {
    // Se itera sobre los productos seleccionados y se elimina uno por uno
    for (const product of selectedProducts) {
      try {
        await deleteProduct(product.id);
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Producto eliminado con éxito'
        );
      } catch (error) {
        console.error(error);
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al eliminar el producto'
        );
      }
    }
    // Después de eliminar, se limpia la selección y se actualiza la lista de productos
    setSelectedProducts([]);
    refreshProducts();
  };

  const editHandler = () => {
    navigate('/producto/' + selectedProducts[0].id);
  };
  return (
    <div>
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
                onClick={editHandler}
              >
                <p className="text-blue">Editar producto</p>
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
        value={productos}
        tableStyle={{ minWidth: '50rem' }}
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
        <Column
          header="Producto"
          body={(rowData: any) => (
            <div className="flex items-center gap-4">
              <Image
                src="https://static.wixstatic.com/media/8c690e_55a384dd4ad142f185b68a029e397ca6~mv2.png/v1/fill/w_570,h_570,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/8c690e_55a384dd4ad142f185b68a029e397ca6~mv2.png"
                alt="Image"
                width="75"
                preview
              />

              <p>{rowData.descripcion}</p>
            </div>
          )}
        />
        <Column field="referencia_interna" header="PReferencia interna" />
        <Column field="preunitario" header="Precio unitario" />
        <Column field="precio_venta" header="Precio venta" />
        <Column field="stock" header="Stock" />
        <Column field="fecha_vencimiento" header="Fecha vencimiento" />
      </DataTable>
      <CustomToast ref={toastRef} />
    </div>
  );
};
