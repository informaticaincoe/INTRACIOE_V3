import React, { useRef, useState } from 'react';
import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate } from 'react-router';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Pagination } from '../../../../shared/interfaces/interfacesPagination';
import { Paginator } from 'primereact/paginator';
import { ReceptorResult } from '../interfaces/receptorInterfaces';

interface TableReceptoresProps {
  updateList: () => void
  pagination: Pagination;
  onPageChange: (event: any) => void;
  receptores: ReceptorResult[];
  setSelectedReceptores: any;
  selectedReceptores: any;
  onDelete: () => void;
  onEdit: () => void;
}

export const TableReceptores: React.FC<TableReceptoresProps> = ({
  receptores,
  onDelete,
  selectedReceptores,
  setSelectedReceptores,
  onEdit,
  onPageChange,
  pagination,
  updateList
}) => {
  const [rowClick] = useState<boolean>(true);
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

  return (
    <div>
      {selectedReceptores.length > 0 && ( // Verificar si hay productos seleccionados
        <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
          <p className="text-blue flex items-center gap-2">
            <FaCheckCircle className="" />
            receptores seleccionados {selectedReceptores.length}
          </p>
          <span className="flex gap-2">
            {selectedReceptores.length === 1 && (
              <span
                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={onEdit}
              >
                <p className="text-blue">Editar producto</p>
              </span>
            )}
            {
              <button
                className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={onDelete}
              >
                <p className="text-red">Eliminar</p>
              </button>
            }
          </span>
        </div>
      )}
      <DataTable
        value={receptores}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode={rowClick ? null : 'multiple'}
        selection={selectedReceptores!}
        onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
          setSelectedReceptores(e.value)
        }
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          selectionMode="multiple"
          headerStyle={{ width: '3rem' }}
        ></Column>
        <Column field="nombre" header="Nombre" />
        <Column field="correo" header="Correo" />
        <Column field="num_documento" header="Documento de identificacion" />
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
      <CustomToast ref={toastRef} />
    </div>
  );
};
