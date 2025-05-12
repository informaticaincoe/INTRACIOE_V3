import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect, useState } from 'react';
import { DevolucionCompraResult } from '../interfaces/devolucionCompraInterfaces';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { Paginator } from 'primereact/paginator';
import { ModalDetallesCompraDevuelta } from './modalDetallesCompraDevuelta';
import { LuExternalLink } from 'react-icons/lu';

interface TablaDevolucionesCompraProps {
  devolucionesList: DevolucionCompraResult[] | undefined;
  updateList: () => void;
  pagination: Pagination;
  onPageChange: (event: any) => void;
}

export const TablaDevolucionesCompra: React.FC<
  TablaDevolucionesCompraProps
> = ({ devolucionesList, pagination, onPageChange }) => {
  const [selectedDevolucionVenta, setSelectedDevolucionVenta] = useState<DevolucionCompraResult>();
  const [visibleModal, setVisibleModal] = useState(false);

  useEffect(() => {
  }, [selectedDevolucionVenta])

  const handleDevolucionSelected = (elemento: any) => {
    setSelectedDevolucionVenta(elemento);
    setVisibleModal(true)
  };

  return (
    <>
      <DataTable
        value={devolucionesList}
        tableStyle={{ minWidth: '50rem' }}
      >
        <Column header="Compra"
          body={(rowData: any) => (
            <button className='flex gap-2 items-center text-blue underline hover:cursor-pointer' onClick={()=>handleDevolucionSelected(rowData)}>
              <LuExternalLink />
              {rowData.compra}
            </button>
          )}
        ></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="motivo" header="Motivo"></Column>
        <Column field="estado" header="Estado"></Column>
        <Column field="usuario" header="Usuario"></Column>
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

      {selectedDevolucionVenta && (
        <ModalDetallesCompraDevuelta
          id={(selectedDevolucionVenta.compra).toString()}
          visible={visibleModal}
          setVisible={setVisibleModal}
        />
      )}
    </>
  );
};
