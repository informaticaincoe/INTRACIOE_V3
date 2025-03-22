import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import React, { useState } from 'react';
import { Product, productosData } from '../FE/productosAgregados/productosData';
import { InputNumber, InputNumberValueChangeEvent } from 'primereact/inputnumber';

export const TablaProductosCreditoFiscal = ({ }) => {
  const [products, setProducts] = useState<Product[]>(productosData);

  // Función para manejar cambios en la cantidad de un producto específico
  const handleCantidadChange = (value: number | null, productId: number) => {
    setProducts(prevProducts =>
      prevProducts.map(product =>
        product.id === productId ? { ...product, cantidad: value ?? 0 } : product
      )
    );
  };

  // Función para manejar cambios en el descuento de un producto específico
  const handleDescuentoChange = (value: number | null, productId: number) => {
    setProducts(prevProducts =>
      prevProducts.map(product =>
        product.id === productId ? { ...product, descuento: value ?? 0 } : product
      )
    );
  };
  
  return (
    <>
      <DataTable
        value={products}
        tableStyle={{ minWidth: '50rem' }}
        paginator
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          field="descripcion"
          header={<p className="text-sm">PRODUCTO</p>}
        ></Column>
        <Column
          body={(rowData: Product) => <p>$ {rowData.precio_unitario}</p>}
          header={<p className="text-sm">PRECIO UNITARIO</p>}
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
