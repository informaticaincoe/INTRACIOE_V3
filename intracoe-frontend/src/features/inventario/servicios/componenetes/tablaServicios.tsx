import React, { useEffect, useRef, useState } from 'react';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';

import CustomToast, {
  CustomToastRef,
  ToastSeverity,
} from '../../../../shared/toast/customToast';
import { useNavigate } from 'react-router';
import { deleteProduct } from '../../products/services/productsServices';

export interface TablaServiciosProps {
  servicios: ProductoResponse[];
  refreshServicios: () => void;
}

export const TablaServicios: React.FC<TablaServiciosProps> = ({
  servicios,
  refreshServicios,
}) => {
  useEffect(() => {
    console.log(servicios);
  }, [servicios]);

  const [rowClick] = useState<boolean>(true);
  const [selectedServices, setSelectedServices] = useState<any[]>([]);
  const toastRef = useRef<CustomToastRef>(null);
  const navigate = useNavigate();

  const handleAccion = (
    severity: ToastSeverity,
    icon: any,
    summary: string
  ) => {
    toastRef.current?.show({
      severity: severity,
      summary: summary,
      icon: icon,
      life: 2000,
    });
  };

  const handleDelete = async () => {
    // Se itera sobre los servicios seleccionados y se elimina uno por uno
    for (const servicio of selectedServices) {
      try {
        await deleteProduct(servicio.id);
        handleAccion(
          'success',
          <FaCheckCircle size={38} />,
          'Servicio eliminado con éxito'
        );
      } catch (error) {
        console.error(error);
        handleAccion(
          'error',
          <IoMdCloseCircle size={38} />,
          'Error al eliminar el Servicio'
        );
      }
    }
    // Después de eliminar, se limpia la selección y se actualiza la lista de servicios
    setSelectedServices([]);
    refreshServicios();
  };

  const editHandler = () => {
    navigate('/servicio/' + selectedServices[0].id);
  };
  return (
    <div>
      {selectedServices.length > 0 && ( // Verificar si hay servicios seleccionados
        <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
          <p className="text-blue flex items-center gap-2">
            <FaCheckCircle className="" />
            servicios seleccionados {selectedServices.length}
          </p>
          <span className="flex gap-2">
            {selectedServices.length === 1 && (
              <span
                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={editHandler}
              >
                <p className="text-blue">Editar producto</p>
              </span>
            )}
            {
              <button
                className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                onClick={handleDelete}
              >
                <p className="text-red">Eliminar</p>
              </button>
            }
          </span>
        </div>
      )}
      <DataTable
        value={servicios}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode={rowClick ? null : 'multiple'}
        selection={selectedServices!}
        onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
          setSelectedServices(e.value)
        }
      >
        <Column
          selectionMode="multiple"
          headerStyle={{ width: '3rem' }}
        ></Column>
        <Column field="codigo" header="Código" />
        <Column field="descripcion" header="Descripcion servicio" />
        <Column field="preunitario" header="Precio unitario servicio" />
        <Column field="precio_venta" header="Precio venta servicio" />
        <Column field="preunitario" header="Precio por servicio" />
      </DataTable>
      <CustomToast ref={toastRef} />
    </div>
  );
};
