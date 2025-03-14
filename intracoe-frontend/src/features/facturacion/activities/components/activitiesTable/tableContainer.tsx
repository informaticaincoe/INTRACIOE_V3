import { useEffect, useState } from 'react';
import { ActivitiesData } from '../../interfaces/activitiesData';
import { TableData } from './tableData';
import { HeaderTable } from '../headerTable/headerTable';
import { WhiteSectionsPage } from '../../../../../shared/containers/whiteSectionsPage';
import { getAllActivities } from '../../services/activitiesServices';

//datos de prueba
const activityList = [
  {
    codigo: '46375',
    descripcion: 'Venta al por mayor de productos lacteos',
  },
  {
    codigo: '47816',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47815',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47814',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47813',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47810',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47816',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47815',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47814',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47813',
    descripcion: 'Venta al por menor de bebidas',
  },
  {
    codigo: '47810',
    descripcion: 'Venta al por menor de bebidas',
  },
];

export const TableContainer = () => {
  const [activities, setActivities] = useState<ActivitiesData[]>([]);

  //consumo de api
  useEffect(() => {
    setActivities(activityList);
    fetchActivities()
  }, []);

  const fetchActivities =()=>{
    getAllActivities()
  }

  return (
    <WhiteSectionsPage>
      <>
        <HeaderTable />
        <TableData activities={activities} />
      </>
    </WhiteSectionsPage>
  );
};
