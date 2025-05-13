import { Dialog } from 'primereact/dialog';
import { getAllReceptor } from '../../../../../../shared/services/receptor/receptorServices';
import { ReceptorInterface } from '../../../../../../shared/interfaces/interfaces';
import { FormReceptoresContainer } from '../../../../../ventas/receptores/components/form/formReceptoresContainer';
import { Toast } from 'primereact/toast';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import React, { useEffect, useRef, useState } from 'react';
import { ReceptorResult } from '../../../../../ventas/receptores/interfaces/receptorInterfaces';

interface StepperProps {
  receptor: ReceptorInterface;
  setReceptor: (receptor: ReceptorInterface) => void;
  errorReceptor: boolean;
  setErrorReceptor: any;
}

interface Pagination {
  count: number;
  current_page: number;
  page_size: number;
  has_next: boolean;
  has_previous: boolean;
}

export const SelectReceptor: React.FC<StepperProps> = ({
  receptor,
  setReceptor,
  errorReceptor,
  setErrorReceptor,
}) => {
  const [receptoresList, setReceptoreLists] = useState<any[]>([]);
  const [visibleModal, setVisibleModal] = useState(false);
  const [updateReceptores, setUpdateReceptores] = useState(false);
  const [visibleTable, setVisibleTable] = useState(false);
  const toast = useRef<Toast>(null);

  const [pagination, setPagination] = useState<Pagination>({
    count: 1,
    current_page: 1,
    page_size: 10,
    has_next: true,
    has_previous: false,
  });

  useEffect(() => {
    fetchReceptores(pagination.current_page, pagination.page_size);
  }, [updateReceptores]);

  const fetchReceptores = async (page: number, limit: number) => {
    try {
      const response = await getAllReceptor({ page, limit });
      setReceptoreLists(response.results); // asumiendo `results` contiene los datos
      setPagination({
        count: response.count,
        current_page: page,
        page_size: limit,
        has_next: response.has_next,
        has_previous: response.has_previous,
      });
    } catch (error) {
      console.error(error);
    }
  };

  const handlePageChange = (event: any) => {
    const page = event.page + 1;
    fetchReceptores(page, pagination.page_size);
  };

  const handleModalSuccess = () => {
    toast.current?.show({
      severity: 'success',
      summary: 'Receptor creado',
      detail: 'Se ha guardado correctamente',
      life: 3000,
    });
    setUpdateReceptores((prev) => !prev);
  };

  const handleRowSelect = (e: any) => {
    setReceptor(e.data);
    if (errorReceptor) setErrorReceptor(false);
    setVisibleTable(false);
  };

  return (
    <>
      <div className="flex flex-col items-start gap-1">
        <label className="opacity-70">Receptor</label>
        <div className="flex w-full justify-between gap-10">
          <button
            onClick={() => { fetchReceptores(1, pagination.page_size), setVisibleTable(true) }}
            className={`w-full text-start border border-border-color rounded-md px-5 py-3 ${errorReceptor ? 'p-invalid' : ''}`}
          >
            {receptor.nombre ? `${receptor.nombre}` : <p className='opacity-75'>Seleccionar receptor</p>}
          </button>
          <button
            className="bg-primary-blue rounded-md px-5 py-2 text-nowrap text-white hover:cursor-pointer"
            onClick={() => setVisibleModal(true)}
          >
            Añadir nuevo receptor
          </button>
        </div>
        {errorReceptor && (
          <p className="text-red">Campo receptor no debe estar vacío</p>
        )}
      </div>

      <Dialog
        header="Seleccionar Receptor"
        visible={visibleTable}
        style={{ width: '70vw' }}
        modal
        onHide={() => setVisibleTable(false)}
      >
        <DataTable
          value={receptoresList}
          paginator
          rows={pagination.page_size}
          totalRecords={pagination.count}
          first={(pagination.current_page - 1) * pagination.page_size}
          onPage={handlePageChange}
          selectionMode="single"
          selection={receptor}
          onRowSelect={handleRowSelect}
          dataKey="id"
          lazy
        >
          <Column
            selectionMode="single"
            headerStyle={{ width: '3rem' }}
          ></Column>
          <Column field="nombre" header="Nombre" sortable />
          <Column field="nombre" header="Nombre" sortable />
          <Column field="nrc" header="NRC" sortable />
          <Column field="correo" header="Correo" />
        </DataTable>
      </Dialog>

      <Dialog
        visible={visibleModal}
        modal
        style={{ width: '50vw',margin: 0 }}
        onHide={() => setVisibleModal(false)}
      >
        <FormReceptoresContainer onSuccess={handleModalSuccess} />
      </Dialog>

      <Toast ref={toast} />
    </>
  );
};