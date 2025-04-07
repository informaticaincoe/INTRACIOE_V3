import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TablaContainerProductos } from '../componentes/tablaContainerProductos';

import { Divider } from 'primereact/divider';
import { TablaProductosHeader } from '../componentes/tablaProductosHeader';

export const ProductsPage = () => {
  return (
    <>
      <Title text="Productos" />
      <WhiteSectionsPage>
        <div>
          <TablaProductosHeader />
          <Divider />
          <TablaContainerProductos />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
