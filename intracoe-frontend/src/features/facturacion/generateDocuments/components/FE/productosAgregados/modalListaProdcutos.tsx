import { Divider } from 'primereact/divider';
import { Checkbox, CheckboxChangeEvent } from 'primereact/checkbox';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { useEffect, useState } from 'react';
import {
  InputNumber,
  InputNumberValueChangeEvent,
} from 'primereact/inputnumber';
import { SendFormButton } from '../../../../../../shared/buttons/sendFormButton';
import { ProductosTabla } from './productosData';

interface ModalListProductsInterface {
  visible: boolean;
  setVisible: (v: boolean) => void;
  listProducts: ProductosTabla[];
  selectedProducts: ProductosTabla[];
  setSelectedProducts: (ps: ProductosTabla[]) => void;
  tipoDte: string
}

export const ModalListaProdcutos: React.FC<ModalListProductsInterface> = ({
  visible,
  setVisible,
  listProducts,
  selectedProducts,
  setSelectedProducts,
  tipoDte
}) => {
  // Solo un estado: la lista completa con sus flags
  const [products, setProducts] = useState<
    (ProductosTabla & { seleccionar: boolean; cantidad: number })[]
  >([]);

  useEffect(() => {
    const merged = listProducts.map((prod) => {
      const sel = selectedProducts.find((p) => p.id === prod.id);
      return {
        ...prod,
        seleccionar: Boolean(sel),
        cantidad: sel?.cantidad ?? 1,
      };
    });
    setProducts(merged);
  }, [listProducts, selectedProducts]);

  // Marca/desmarca
  const onSelectChange = (e: CheckboxChangeEvent, id: number) => {
    setProducts((prev) =>
      prev.map((p) =>
        p.id === id ? { ...p, seleccionar: e.checked ?? false } : p
      )
    );
  };

  // Cambia cantidad
  const onCantidadChange = (e: InputNumberValueChangeEvent, id: number) => {
    const nueva = e.value ?? 1;
    setProducts((prev) =>
      prev.map((p) => (p.id === id ? { ...p, cantidad: nueva } : p))
    );
  };

  const guardar = () => {
    const seleccionados = products.filter((p) => p.seleccionar);
    const IVA = 0.13;
  
    const productosConTotales = seleccionados.map((producto) => {
      const cantidad = producto.cantidad;
  
      // Aseguramos que el precio unitario usado para visualización y totales
      let preUnitario: number;
  
      // Precio mostrado y total depende del tipo de DTE y si ya tiene IVA
      if (tipoDte === '01') {
        // Para consumidor final, el precio final debe incluir IVA
        preUnitario = producto.precio_iva
          ? producto.preunitario // ya viene con IVA incluido
          : producto.preunitario * (1 + IVA); // agregamos IVA
      } else {
        // Para crédito fiscal, el precio se deja tal cual, ya sea con o sin IVA, se desglosa después
        preUnitario = producto.preunitario;
      }
  
      const baseUnit = producto.precio_iva
        ? producto.preunitario / (1 + IVA)
        : producto.preunitario;
  
      const total_neto = baseUnit * cantidad;
      const total_iva = total_neto * IVA;
      const total_con_iva = total_neto + total_iva;
  
      return {
        ...producto,
        preunitario: preUnitario,
        total_neto: tipoDte === '01' ? total_con_iva : total_neto,
        total_iva,
        total_con_iva,
      };
    });
  
    setSelectedProducts(productosConTotales);
    setVisible(false);
  };
  

  const footer = (
    <div className="flex justify-end gap-2">
      <SendFormButton
        onClick={guardar}
        text="Agregar"
        className="bg-primary-blue px-10 text-white"
      />
      <SendFormButton
        onClick={() => setVisible(false)}
        text="Cerrar"
        className="border-primary-blue border px-10"
      />
    </div>
  );

  return (
    <Dialog
      visible={visible}
      modal
      header={
        <>
          <h1 className="text-2xl font-bold">Seleccionar productos</h1>
          <Divider className="m-0 p-0" />
        </>
      }
      footer={footer}
      style={{ width: '80%' }}
      onHide={() => setVisible(false)}
    >
      <DataTable
        value={products}
        tableStyle={{ minWidth: '50rem' }}
        paginator
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          header="SELECCIONAR"
          body={(row: any) => (
            <Checkbox
              checked={row.seleccionar}
              onChange={(e) => onSelectChange(e, row.id)}
            />
          )}
        />
        <Column
          header="PRODUCTO"
          body={(row: any) => <span>{row.descripcion}</span>}
        />
        <Column
          header="PRECIO UNITARIO"
          body={(row: any) => <span>{row.preunitario}</span>}
        />
        <Column
          header="CANTIDAD"
          body={(row: any) => (
            <InputNumber
              value={row.cantidad}
              onValueChange={(e) => onCantidadChange(e, row.id)}
              className="w-[5rem]"
              min={1}
            />
          )}
        />
      </DataTable>
    </Dialog>
  );
};
