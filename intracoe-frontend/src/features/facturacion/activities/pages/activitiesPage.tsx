import { useEffect, useState } from 'react';
import { Title } from '../../../../shared/text/title';
import { TableContainer } from '../components/activitiesTable/tableContainer';
import { getAllActivities } from '../../../../shared/catalogos/services/catalogosServices';

export const ActivitiesPage = () => {
  const [actividades, setActividades] = useState();

  useEffect(() => {
    fetchActividadesEconomicas();
  }, []);

  const fetchActividadesEconomicas = async () => {
    try {
      const response = await getAllActivities();
      setActividades(response);
    } catch (error) {
      console.log(error);
    }
  };
  return (
    <div>
      <Title text="Actividades economicas" />
      <TableContainer data={actividades} />
    </div>
  );
};
