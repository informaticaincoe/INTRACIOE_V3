import { Title } from '../../../../shared/text/title';
import { TableContainer } from '../components/activitiesTable/tableContainer';

export const ActivitiesPage = () => {
  return (
    <div className="py-8">
      <Title text="Actividades economicas" />
      <TableContainer />
    </div>
  );
};
