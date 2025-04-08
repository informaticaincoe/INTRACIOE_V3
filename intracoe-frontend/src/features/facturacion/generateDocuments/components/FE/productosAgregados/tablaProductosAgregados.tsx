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
import { getAllDescuentos } from '../../../../../../shared/services/productos/productosServices';
import { Dropdown } from 'primereact/dropdown';

interface TablaProductosAgregadosProps {
  setListProducts: any;
  listProducts: ProductosTabla[];
  setCantidadListProducts: any;
  setIdListProducts: any;
  setDescuentoItem: any;
  descuentoItem: number;
  tipoDte: any;
  descuentosList: any
}

export const TablaProductosAgregados: React.FC<
  TablaProductosAgregadosProps
> = ({
  setListProducts,
  listProducts,
  setCantidadListProducts,
  setIdListProducts,
  setDescuentoItem,
  tipoDte,
  descuentosList
}) => {
    const [auxSelectedProducts, setAuxSelectedProducts] = useState<any[]>([]); //para almacenar los filas seleccionadas
    const [rowClick] = useState<boolean>(true); //detectar una fila selecionada
    const [visibleDeleteModal, setVisibleDeleteModal] = useState<boolean>(false);
    const [visibleTributoModal, setVisibleTributoModal] = useState<boolean>(false);


    useEffect(() => {
      fetchDescuento();
    }, []);

    useEffect(() => {
      const auxId = listProducts.map((product) => product.id);
      const auxCantidad = listProducts.map((product) => product.cantidad);
      const auxDescuento = listProducts.map((product) => product.descuento?.porcentaje);
      console.log(auxDescuento)

      console.log(auxCantidad)

      setCantidadListProducts(auxCantidad);
      setIdListProducts(auxId);
      setDescuentoItem(auxDescuento)
    }, [listProducts]);

    const calcularTotales = (prod: ProductosTabla): ProductosTabla => {
      const IVA_RATE = 0.13;
      const qty = prod.cantidad;
      const salePrice = prod.precio_venta;   // ahora tomamos el precio real
      const hasIva = prod.precio_iva;     // booleano

      // 1) Obtener el porcentaje de descuento
      let descPct = 0;
      if (prod.descuento) {
        if (typeof prod.descuento === 'object' && 'porcentaje' in prod.descuento) {
          descPct = prod.descuento.porcentaje || 0;
        } else {
          descPct = Number(prod.descuento) || 0;
        }
      }

      // 2) Extraer el precio base sin IVA si el precio de venta ya lo incluye
      const baseUnit = hasIva
        ? salePrice / (1 + IVA_RATE)
        : salePrice;

      // 3) Subtotal sin IVA
      const subTotal = baseUnit * qty;
      // 4) Descuento sobre ese subtotal
      const discountAmount = subTotal * descPct;
      const netAfterDisc = subTotal - discountAmount;

      // 5) IVA sobre el neto con descuento
      const ivaAmount = netAfterDisc * IVA_RATE;
      // 6) Total con IVA
      const totalWithIva = netAfterDisc + ivaAmount;

      console.log(totalWithIva)


      if (tipoDte === '01') {
        // Consumidor final: consideramos "neto" = total con IVA
        return {
          ...prod,
          total_neto: totalWithIva,
          total_iva: ivaAmount,
          total_con_iva: totalWithIva,
        };
      } else {
        // Crédito fiscal: neto sin IVA, IVA por separado
        return {
          ...prod,
          total_neto: netAfterDisc,
          total_iva: ivaAmount,
          total_con_iva: totalWithIva,
        };
      }
    };


    // Función para manejar cambios en la cantidad de un producto específico
    const handleCantidadChange = (value: number | null, productId: number) => {
      const nuevaCantidad = value ?? 1;
      setListProducts((prev: any[]) =>
        prev.map(p =>
          p.id === productId
            ? calcularTotales({ ...p, cantidad: nuevaCantidad })
            : p
        )
      );
    };

    const handleDescuentoChange = (value: string, productId: number) => {
      setListProducts((prev: any[]) =>
        prev.map(p =>
          p.id === productId
            ? calcularTotales({ ...p, descuento: value })
            : p
        )
      );
    };


    const handleDelete = () => {
      console.log('auxSelectedProducts', auxSelectedProducts);
      setVisibleDeleteModal(true);
    };

    const handleTributosModal = () => {
      setVisibleTributoModal(true);
    };

    const handlerEliminarItem = () => {
      // Filtrar los productos que NO están seleccionados
      const filterList = listProducts.filter((product) => {
        // Verificar si el producto no está en auxSelectedProducts
        return !auxSelectedProducts.some((item) => product.id === item.id);
      });
      setListProducts(filterList); // Actualizar la lista de productos
      setAuxSelectedProducts([]); // Limpiar los productos seleccionados
      setVisibleDeleteModal(false);
    };

    const fetchDescuento = async () => {
      try {
        const response = await getAllDescuentos();
        // setDescuentosList(response);
        console.log("ZZZZZZZZZZZZZZZZZZZZZZZZZZ", descuentosList)
        // Solo asignas si ya existían productos (evitar reescritura innecesaria)
        setAuxSelectedProducts((prevProducts: any[]) =>
          prevProducts.map((product) => ({
            ...product,
            descuento: product.descuento ?? '0',
          }))
        );
      } catch (error) {
        console.log(error);
      }
    };

    return (
      <>
        {auxSelectedProducts.length > 0 && ( // Verificar si hay productos seleccionados
          <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
            <p className="text-blue flex items-center gap-2">
              <FaCheckCircle className="" />
              productos seleccionados {auxSelectedProducts.length}
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
          size={auxSelectedProducts.length}
          onClick={handlerEliminarItem}
        />

        <ModalAgregarTributo
          setVisible={setVisibleTributoModal}
          visible={visibleTributoModal}
        />

        <DataTable
          key={tipoDte}
          value={listProducts}
          tableStyle={{ minWidth: '50rem' }}
          paginator
          rows={5}
          rowsPerPageOptions={[5, 10, 25, 50]}
          selectionMode={rowClick ? null : 'multiple'}
          selection={auxSelectedProducts!}
          onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
            setAuxSelectedProducts(e.value)
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
          {tipoDte == '03' && (
            <Column
              body={(rowData: ProductosTabla) => (
                <p>$ {rowData.preunitario}</p>
              )}
              header={<p className="text-sm">PRECIO UNITARIO</p>}
            ></Column>
          )}
          {tipoDte == '03' && (
            <Column
              body={(rowData: ProductosTabla) => {
                if (rowData.precio_iva)
                  return <p>$ {rowData.preunitario / 1.13}</p>;
                else
                  return <p>$ {rowData.cantidad * 0.13}</p>;
              }}
              header={<p className="text-sm">IVA UNITARIO</p>}
            ></Column>
          )}
          {tipoDte == '01' && (
            <Column
              header={<p className="text-sm">PRECIO UNITARIO</p>}
              body={(rowData: ProductosTabla) => {
                return <p>$ {(rowData.preunitario * 1.13).toFixed(2)}</p>; // incluir e iva en el precio si es consumidor final
              }}
            />
          )}
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
                options={descuentosList} // sólo porcentajes
                optionLabel='porcentaje'
                placeholder="Seleccione un descuento"
                className="md:w-14rem w-full"
              />
            )}
          />

          <Column
            body={(rowData: ProductosTabla) => <p>$ {rowData.total_tributos}</p>}
            header={<p className="text-sm uppercase">TOTAL tributos</p>}
          ></Column>

          {tipoDte == '01' &&
            <Column
              header="TOTAL"
              body={(rowData) => {
                return <p>$ {(rowData.total_con_iva).toFixed(2)}</p>;
              }}
            />}
          {tipoDte == '03' &&
            <Column
              header="TOTAL NETO"
              body={(rowData) => {

                return <span>$ {rowData.total_neto.toFixed(2)}</span>;
              }}
            />}
          {tipoDte == '03' &&
            <Column
              header="TOTAL IVA"
              body={(rowData) => {

                return <span>$ {rowData.total_iva.toFixed(2)}</span>;
              }}
            />}

          {tipoDte == '03' &&
            <Column
              header="TOTAL CON IVA"
              body={(row) => {

                return <span>$ {row.total_con_iva.toFixed(2)}</span>;
              }}
            />}
        </DataTable >
      </>
    );
  };