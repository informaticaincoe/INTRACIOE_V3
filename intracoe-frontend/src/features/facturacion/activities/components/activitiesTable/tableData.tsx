import { ActivitiesData } from '../../interfaces/activitiesData';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
// import 'primereact/resources/themes/tailwind-light/theme.css';
import 'primereact/resources/themes/lara-light-blue/theme.css';

//icons
import { IoEyeOutline } from 'react-icons/io5';
import { MdDeleteOutline } from 'react-icons/md';
import { DeleteModal } from '../../../../../shared/modal/deleteModal';
import { useState } from 'react';
import { ViewModal } from '../../../../../shared/modal/viewModal';

interface ActivitiesProps {
  activities: ActivitiesData[];
}

export const TableData: React.FC<ActivitiesProps> = ({ activities }) => {
  const [actionType, setActionType] = useState<
    'edit' | 'view' | 'delete' | null
  >(null);
  const [selectedActivity, setSelectedActivity] =
    useState<ActivitiesData | null>(null);

  const handleSelect = (activity: ActivitiesData, type: any) => {
    setSelectedActivity(activity);
    setActionType(type);
  };

  const actions = (activity: ActivitiesData) => {
    return (
      <div className="group flex gap-5 text-sm">
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => {
            handleSelect(activity, 'view');
          }}
        >
          <IoEyeOutline size={20} color="#7C7C7C" />
          <p className="text-gray">Ver</p>
        </button>
        <button
          className="flex items-center gap-1 hover:cursor-pointer"
          onClick={() => handleSelect(activity, 'delete')}
        >
          <MdDeleteOutline size={20} color="#FC0005" />
          <p className="text-red">Eliminar</p>
        </button>
      </div>
    );
  };

  return (
    <>
      <DataTable
        value={activities}
        paginator
        rows={5}
        rowsPerPageOptions={[5, 10, 25, 50]}
      >
        <Column
          field="codigo"
          header={<p className="text-black">CODIGO</p>}
        ></Column>
        <Column
          field="descripcion"
          header={<p className="text-black">DESCRIPCIÓN</p>}
        ></Column>
        <Column
          header={<p className="text-black">ACCIONES</p>}
          body={actions}
        ></Column>
      </DataTable>

      {/* Solo renderiza el modal si hay una actividad seleccionada */}
      {selectedActivity && actionType == 'delete' && (
        <DeleteModal
          activity={selectedActivity}
          onClose={() => setSelectedActivity(null)}
        />
      )}
      {selectedActivity && actionType == 'view' && (
        <ViewModal
          activity={selectedActivity}
          onClose={() => setSelectedActivity(null)}
        />
      )}
    </>
  );
};