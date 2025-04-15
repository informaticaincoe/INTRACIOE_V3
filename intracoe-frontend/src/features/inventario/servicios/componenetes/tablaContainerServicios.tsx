import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { TablaServicios } from './tablaServicios';

interface TablaContainerServiciosProps {
  servicios: ProductoResponse[];
  refreshServicios: () => void;
}

export const TablaContainerServicios: React.FC<
  TablaContainerServiciosProps
> = ({ servicios, refreshServicios }) => {
  return (
    <TablaServicios servicios={servicios} refreshServicios={refreshServicios} />
  );
};
