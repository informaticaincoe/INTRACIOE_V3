import React, { useEffect, useState } from 'react';
import { AjusteInventarioInterface, AjusteInventarioInterfaceResults } from '../interfaces/ajusteInventarioInterfaces';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { Paginator } from 'primereact/paginator';
import { LuExternalLink } from 'react-icons/lu';
import { ModalDetalleMovimientoInventario } from '../../movimientoInventario/componentes/modalDetalleMovimientoInventario';
import { classNames } from 'primereact/utils';
import { ModalDetalleAjusteMovimientoInventario } from './modalDetalleAjusteMovimientoInventario';

interface TablaAjusteInventarioProps {
  ajusteInventario: any;
  updateList: () => void;
  pagination: Pagination;
  onPageChange: (event: any) => void;
}

export const TablaAjusteInventario: React.FC<TablaAjusteInventarioProps> = ({
  ajusteInventario,
  updateList,
  pagination,
  onPageChange,
}) => {
  const [visibleModal, setVisibleModal] = useState(false);
  const [selectedAjustesInventario, setSelectedAjustesInventario] =
    useState<AjusteInventarioInterfaceResults | null>(null);
  const [detalleMovimiento, setDetalleMovimiento] = useState<number>()
  const [viewDetalleMovimientoModal, setViewDetalleMovimientoModal] = useState(false)

  useEffect(() => {
    setVisibleModal(true);
    if (selectedAjustesInventario) console.log("dataEDITTT", selectedAjustesInventario);
  }, [selectedAjustesInventario]);

  const handleDetallesMovimeinto = (id: any) => {
    console.log(id)
    setDetalleMovimiento(id)
    setViewDetalleMovimientoModal(true)
  }

  return (
    <>
      <DataTable
        value={ajusteInventario}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode="single"
        selection={selectedAjustesInventario} // Se maneja como un único objeto de tipo movimientoInterface
        onSelectionChange={(e) =>
          setSelectedAjustesInventario(
            e.value ? (e.value as AjusteInventarioInterfaceResults) : null
          )
        }
        dataKey="id"
      >
        <Column
          header="Movimiento"
          body={(rowData: any) => (
            <button onClick={() => handleDetallesMovimeinto(rowData.movimiento)} className='flex gap-1 text-blue items-center'>
              <LuExternalLink />
              {rowData.movimiento}
            </button>
          )}
        ></Column>
        <Column field="nombreProducto" header="Producto"></Column>
        <Column field="cantidad_ajustada" header="Cantidad"></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="nombreAlmacen" header="Almacen"></Column>
        <Column field="usuario" header="Usuario"></Column>

      </DataTable >

      <div className="pt-5">
        <Paginator
          first={(pagination.current_page - 1) * pagination.page_size}
          rows={pagination.page_size}
          totalRecords={pagination.count}
          rowsPerPageOptions={[10, 25, 50]}
          onPageChange={onPageChange}
        />
      </div>

      {
        selectedAjustesInventario && (
          <ModalDetalleAjusteMovimientoInventario
            data={selectedAjustesInventario} // Solo pasa un ID válido si hay un producto seleccionado
            visible={visibleModal}
            setVisible={setVisibleModal}
          />
        )
      }
      {
        detalleMovimiento && (
          <ModalDetalleMovimientoInventario id={detalleMovimiento} visible={viewDetalleMovimientoModal} setVisible={setViewDetalleMovimientoModal} />
        )}
    </>
  );
};
