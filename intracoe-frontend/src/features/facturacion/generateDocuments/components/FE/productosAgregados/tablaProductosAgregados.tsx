import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect, useState } from 'react';
import { ProductosTabla } from './productosData';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import './InputNumberCustom.css';
import { FaCheckCircle } from 'react-icons/fa';
import { ModalEliminarItemDeLista } from '../../Shared/modal/modalEliminarItemDeLista';
import { ModalAgregarTributo } from '../../Shared/modal/modalAgregarTributo';
import { getAllDescuentos } from '../../../services/productos/productosServices';
import { Dropdown } from 'primereact/dropdown';

interface TablaProductosAgregadosProps {
  listProducts: ProductosTabla[],
  setListProducts: any,
  setCantidadListProducts: any,
  setIdListProducts: any,
  setDescuentoItem: any,
  descuentoItem: number
}

export const TablaProductosAgregados: React.FC<TablaProductosAgregadosProps> = ({ setListProducts, listProducts, setCantidadListProducts, setIdListProducts }) => {
  const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
  const [rowClick] = useState<boolean>(true);
  const [visibleDeleteModal, setVisibleDeleteModal] = useState<boolean>(false);
  const [visibleTributoModal, setVisibleTributoModal] = useState<boolean>(false);
  const [descuentosList, setDescuentosList] = useState<any[]>([]) // variable para almacenar al lista de descuentos y mostrarla en un dropdown

  useEffect(() => {
    fetchDescuento()
    console.log(listProducts)
  }, [])

  useEffect(() => {
    const auxId = listProducts.map((product) => product.id)
    const auxCantidad = listProducts.map((product) => product.cantidad)

    setCantidadListProducts(auxCantidad)
    setIdListProducts(auxId)

  }, [listProducts]);

  // Función para manejar cambios en la cantidad de un producto específico
  const handleCantidadChange = (value: number | null, productId: number) => {
    setListProducts((prevProducts: any[]) =>
      prevProducts.map((product) => {
        if (product.id === productId) {
          const nuevaCantidad = value ?? 1;
          const totalNeto = product.precio_unitario * nuevaCantidad;
          const totalIVA = product.iva_unitario * nuevaCantidad;
          const totalConIVA = totalNeto + totalIVA;

          return {
            ...product,
            cantidad: nuevaCantidad,
            total_neto: totalNeto,
            total_iva: totalIVA,
            total_con_iva: totalConIVA,
          };
        }
        return product;
      })
    );
  };

  // Función para manejar cambios en el descuento de un producto específico
  const handleDescuentoChange = (value: number | null, productId: number) => {
    setListProducts((prevProducts: any[]) =>
      prevProducts.map((product: { id: number; }) =>
        product.id === productId
          ? { ...product, descuento: value ?? 0 }
          : product
      )
    );

  };

  const handleDelete = () => {
    console.log("selectedProducts", selectedProducts);
    setVisibleDeleteModal(true);
  };

  const handleTributosModal = () => {
    setVisibleTributoModal(true)
  }

  const handlerEliminarItem = () => {
    // Filtrar los productos que NO están seleccionados
    const filterList = listProducts.filter(product => {
      // Verificar si el producto no está en selectedProducts
      return !selectedProducts.some(item => product.id === item.id);
    });

    console.log("filterList", filterList);
    setListProducts(filterList); // Actualizar la lista de productos
    setSelectedProducts([]); // Limpiar los productos seleccionados
    setVisibleDeleteModal(false);
  }

  const fetchDescuento = async () => {
    try {
      const response = await getAllDescuentos()
      setDescuentosList(response)
    } catch (error) {
      console.log(error)
    }
  }


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
            <span
              className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
              onClick={handleTributosModal}
            >
              <p className="text-blue">Agregar tributo</p>
            </span>
          </span>
        </div>
      )}
      <ModalEliminarItemDeLista
        setVisible={setVisibleDeleteModal}
        visible={visibleDeleteModal}
        size={selectedProducts.length}
        onClick={handlerEliminarItem}

      />

      <ModalAgregarTributo
        setVisible={setVisibleTributoModal}
        visible={visibleTributoModal}
      />

      <DataTable
        value={listProducts}
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
          body={(rowData: ProductosTabla) => <p>$ {rowData.precio_unitario}</p>}
          header={<p className="text-sm">PRECIO UNITARIO</p>}
        ></Column>
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.iva_unitario}</p>}
          header={<p className="text-sm">IVA UNITARIO</p>}
        ></Column>
        <Column
          header={<p className="text-sm">CANTIDAD</p>}
          body={(rowData: ProductosTabla) => (
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
          header={<p className="text-sm">DESCUENTO</p>}
          body={(rowData: ProductosTabla) => (
            <Dropdown
              value={rowData.descuento}
              onChange={(e) => handleDescuentoChange(e.value, rowData.id)}
              options={descuentosList}
              optionLabel="porcentaje"
              optionValue="id"
              className="w-full md:w-14rem" />
          )}
        />
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.total_tributos}</p>}
          header={<p className="text-sm uppercase">TOTAL tributos</p>}
        ></Column>
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.total_neto.toFixed(2)}</p>}
          header={<p className="text-sm">TOTAL NETO</p>}
        />
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.total_iva.toFixed(2)}</p>}
          header={<p className="text-sm">TOTAL IVA</p>}
        />
        <Column
          body={(rowData: ProductosTabla) => <p>$ {rowData.total_con_iva.toFixed(2)}</p>}
          header={<p className="text-sm">TOTAL CON IVA</p>}
        />
      </DataTable>
    </>
  );
};
