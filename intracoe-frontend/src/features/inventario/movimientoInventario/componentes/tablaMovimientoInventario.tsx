import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { FaCaretUp } from 'react-icons/fa6';
import {
  movimientoInterface,
  resultsMovimiento,
} from '../interfaces/movimientoInvetarioInterface';
import { ModalDetalleMovimientoInventario } from './modalDetalleMovimientoInventario';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { Paginator } from 'primereact/paginator';

interface TablaMovimientoInventarioProps {
  movimientoList: resultsMovimiento[] | undefined;
  updateMovimientos: any;
  pagination: Pagination;
  onPageChange: (event: any) => void;
}

export const TablaMovimientoInventario: React.FC<
  TablaMovimientoInventarioProps
> = ({ movimientoList, updateMovimientos, pagination, onPageChange }) => {
  const [visibleModal, setVisibleModal] = useState(false);
  const [selectedProducts, setSelectedProducts] =
    useState<resultsMovimiento | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setVisibleModal(true);
  }, [selectedProducts]);

  return (
    <>
      <DataTable
        value={movimientoList}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode="single"
        selection={selectedProducts} // Se maneja como un único objeto de tipo movimientoInterface
        onSelectionChange={(e) =>
          setSelectedProducts(e.value ? (e.value as any) : null)
        }
        dataKey="id"
      >
        <Column
          header="Tipo"
          body={(rowData: any) => {
            return rowData.tipo === 'Salida' ? (
              <span className="text-red flex gap-2">
                <FaCaretUp className="rotate-180" />
                {rowData.tipo}
              </span>
            ) : (
              <span className="text-green flex gap-2">
                <FaCaretUp className=" " />
                {rowData.tipo}
              </span>
            );
          }}
        ></Column>
        <Column field="nombreProducto" header="Producto"></Column>
        <Column field="cantidad" header="Cantidad"></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="nombreAlmacen" header="Almacen"></Column>
        <Column field="referencia" header="Referencia"></Column>
      </DataTable>
      <div className="pt-5">
        <Paginator
          first={(pagination.current_page - 1) * pagination.page_size}
          rows={pagination.page_size}
          totalRecords={pagination.count}
          rowsPerPageOptions={[10, 25, 50]}
          onPageChange={onPageChange}
        />
      </div>

      {selectedProducts && (
        <ModalDetalleMovimientoInventario
          id={selectedProducts?.id ?? 0} // Solo pasa un ID válido si hay un producto seleccionado
          visible={visibleModal}
          setVisible={setVisibleModal}
        />
      )}
    </>
  );
};
