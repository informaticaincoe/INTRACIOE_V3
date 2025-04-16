import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Title } from '../../../../shared/text/title';
import { TablaContainerProductos } from '../componentes/tablaContainerProductos';

import { Divider } from 'primereact/divider';
import { TablaProductosHeader } from '../componentes/tablaProductosHeader';
import { useEffect, useState } from 'react';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';

export const ProductsPage = () => {
  const [productos, setProductos] = useState<ProductoResponse[]>([]);
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  // Cada vez que cambie el filtro, recargamos los productos
  useEffect(() => {
    fetchProductos();
  }, [codigoFiltro]);

  const fetchProductos = async () => {
    try {
      // Pasamos tipo=1 (productos) y, si hay código, también filter
      const response = await getAllProducts({
        tipo: 1,
        filter: codigoFiltro || undefined,
      });
      setProductos(response);
    } catch (error) {
      console.error(error);
    }
  };

  // Handler que pasamos al header para que active la búsqueda
  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Title text="productos" />
      <WhiteSectionsPage>
        <div>
          <TablaProductosHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaContainerProductos
            productos={productos}
            refreshProducts={fetchProductos}
          />
        </div>
      </WhiteSectionsPage>
    </>
  );
};
