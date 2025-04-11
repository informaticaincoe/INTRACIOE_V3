import { useEffect, useState } from 'react';
import { HeaderTable } from '../headerTable/headerTable';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { getAllActivities } from '../../services/activitiesServices';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import Actions from './actionsTable';
import 'primereact/resources/themes/lara-light-blue/theme.css';
import { ActivitiesData } from '../../../../../shared/interfaces/interfaces';

export const TableContainer = () => {
  const [activities, setActivities] = useState<ActivitiesData[]>([]);
  const [filterTerm, setFilterTerm] = useState<string>('');

  useEffect(() => {
    fetchActivities(filterTerm);
  }, [filterTerm]);


  const fetchActivities = async (filtro = '') => {
    const data = await getAllActivities(filtro);
    setActivities(data);
  };

  const onDelete = () => {
    fetchActivities();
  };

  return (
    <WhiteSectionsPage>
      <>
        <HeaderTable
          setActivities={setActivities}
          filterTerm={filterTerm}
          setFilterTerm={setFilterTerm}
        />
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
            />
            <Column
              field="descripcion"
              header={<p className="text-black">DESCRIPCIÓN</p>}
            />
            <Column
              header="ACCIONES"
              body={(activity: ActivitiesData) => (
                <Actions activity={activity} onDelete={onDelete} />
              )}
            />
          </DataTable>
        </>
      </>
    </WhiteSectionsPage>
  );
};
