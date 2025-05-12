import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { CompraInterface, compraResult } from '../interfaces/comprasInterfaces';
import { IoIosCloseCircleOutline } from 'react-icons/io';
import { FaRegCircleCheck } from 'react-icons/fa6';
import { ModalDetallesCompra } from './modalDetallesCompra';
import { IoWarningOutline } from 'react-icons/io5';
import dayjs from 'dayjs';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { Paginator } from 'primereact/paginator';
import { useNavigate } from 'react-router';

interface TablaComprasProps {
  comprasList: compraResult[] | undefined;
  updateList: () => void;
  pagination: Pagination;
  onPageChange: (event: any) => void;
}

export const TablaCompras: React.FC<TablaComprasProps> = ({
  comprasList,
  updateList,
  pagination,
  onPageChange,
}) => {
  const [selectedCompras, setSelectedCompras] = useState<
    compraResult | undefined
  >();
  const [visibleModal, setVisibleModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setVisibleModal(true);
    if (selectedCompras) console.log('SELECTED COMPRA', selectedCompras);
  }, [selectedCompras]);

  const handleDevolucionSelected = (elemento: any) => {
    console.log(elemento);
    setSelectedCompras(elemento);
    setVisibleModal(true);
  };

  return (
    <>
      <DataTable
        value={comprasList}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode={'single'}
        selection={selectedCompras}
        onSelectionChange={(e) =>
          handleDevolucionSelected(e.value as CompraInterface)
        }
      >
        <Column field="nombreProveedor" header="Proveedor"></Column>
        <Column
          header="fecha y hora"
          body={(rowData: any) => {
            return <p>{dayjs(rowData.fecha).format('DD-MM-YYYY HH:mm:ss')}</p>;
          }}
        />
        <Column
          header="Total"
          body={(rowData: any) => <p>$ {rowData.total}</p>}
        />
        <Column
          header="Estado"
          body={(rowData: any) => {
            if (rowData.estado === 'Pendiente') {
              return (
                <span className="text-primary-yellow flex gap-2">
                  <IoWarningOutline size={20} />
                  {rowData.estado}
                </span>
              );
            }
            if (rowData.estado === 'Pagado') {
              return (
                <span className="text-green flex gap-2">
                  <FaRegCircleCheck size={18} />
                  {rowData.estado}
                </span>
              );
            }
            if (rowData.estado === 'Cancelado') {
              return (
                <span className="text-red flex gap-2">
                  <IoIosCloseCircleOutline size={20} />
                  {rowData.estado}
                </span>
              );
            }
            return null;
          }}
        />
        <Column
          header="Acciones"
          body={(rowData: any) => (
            <>
              <p
                className="text-blue text-start underline"
                onClick={() => handleDevolucionSelected(rowData)}
              >
                Ver detalles
              </p>
              <p
                className="text-blue text-start underline"
                onClick={() => navigate(`/compras/${rowData.id}`)}
              >
                Editar
              </p>
            </>
          )}
        />
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
      {selectedCompras && (
        <ModalDetallesCompra
          data={selectedCompras}
          visible={visibleModal}
          setVisible={setVisibleModal}
        />
      )}
    </>
  );
};
