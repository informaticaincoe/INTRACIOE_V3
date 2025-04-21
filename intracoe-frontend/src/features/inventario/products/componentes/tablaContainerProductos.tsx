import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { TablaProductos } from './tablaProductos';

interface TablaContainerServiciosProps {
  productos: ProductoResponse[];
  refreshProducts: () => void;
}

export const TablaContainerProductos: React.FC<
  TablaContainerServiciosProps
> = ({ productos, refreshProducts }) => {
  return (
    <TablaProductos productos={productos} refreshProducts={refreshProducts} />
  );
};
