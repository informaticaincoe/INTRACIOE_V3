import { useState } from 'react';
import { HeaderTable } from '../headerTable/headerTable';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import 'primereact/resources/themes/lara-light-blue/theme.css';
import { ActivitiesData } from '../../../../../shared/interfaces/interfaces';

interface TableContainerProp {
  data: any;
}

export const TableContainer: React.FC<TableContainerProp> = ({ data }) => {
  const [activities, setActivities] = useState<ActivitiesData[]>([]);
  const [filterTerm, setFilterTerm] = useState<string>('');

  // const onDelete = () => {
  //   fetchActivities();
  // };

  return (
    <div className="px-10 py-5">
      <>
        <HeaderTable
          setActivities={setActivities}
          filterTerm={filterTerm}
          setFilterTerm={setFilterTerm}
        />
        <>
          <DataTable
            value={data}
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
            {/* <Column
              header="ACCIONES"
              body={(activity: ActivitiesData) => (
                <Actionsz activity={activity} onDelete={onDelete} />
              )}
            /> */}
          </DataTable>
        </>
      </>
    </div>
  );
};
