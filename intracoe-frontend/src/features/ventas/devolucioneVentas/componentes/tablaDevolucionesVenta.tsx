import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router';
import { ModalDetallesDevolucionesVenta } from './modalDetallesDevolucionesVenta';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { DevolucionVentaDetalleInterfaceResult } from '../interface/devolucionVentaInterface';
import { DevolucionCompraResult } from '../../../compras/devolucionesCompras/interfaces/devolucionCompraInterfaces';
import { Paginator } from 'primereact/paginator';

interface TablaDevolucionesVentaProps {
  devolucionesList: DevolucionVentaDetalleInterfaceResult[];
  pagination: Pagination;
  updateList: () => void;
  onPageChange: (event: any) => void;
}

export const TablaDevolucionesVenta: React.FC<TablaDevolucionesVentaProps> = ({
  updateList,
  devolucionesList,
  pagination,
  onPageChange,
}) => {
  const [rowClick] = useState<boolean>(true);
  const [selectedDevolucionVenta, setSelectedDevolucionVenta] = useState<
    DevolucionVentaDetalleInterfaceResult | undefined
  >();
  const [visibleModal, setVisibleModal] = useState(false);

  const navigate = useNavigate();

  const handleDevolucionSelected = (elemento: any) => {
    console.log(elemento);
    setSelectedDevolucionVenta(elemento);
    setVisibleModal(true);
  };

  useEffect(() => {
    console.log('AAAAAAAAAAAAAAAAAAAA', pagination);
  }, []);

  return (
    <>
      <DataTable
        value={devolucionesList}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode={'single'}
        selection={selectedDevolucionVenta}
        onSelectionChange={(e) => handleDevolucionSelected(e.value)}
      >
        <Column field="num_factura" header="Factura"></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="motivo" header="Motivo"></Column>
        <Column field="estado" header="Estado"></Column>
        <Column field="usuario" header="Usuario"></Column>
        <Column
          header="Acciones"
          body={(rowData: any) => (
            <button
              className="underline hover:cursor-pointer"
              onClick={() => handleDevolucionSelected(rowData)}
            >
              Ver detalles
            </button>
          )}
        ></Column>
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

      {/* {selectedDevolucionVenta && (
        <ModalDetallesDevolucionesVenta
          data={selectedDevolucionVenta} // Solo pasa un ID válido si hay un producto seleccionado
          visible={visibleModal}
          setVisible={setVisibleModal}
        />
      )} */}
    </>
  );
};
