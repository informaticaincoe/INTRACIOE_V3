import { useEffect, useState } from 'react';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { TablaProductos } from './tablaProductos';

export const TablaContainerProductos = () => {
  const [productos, setProductos] = useState<ProductoResponse[]>([]);

  useEffect(() => {
    fetchProductos();
  }, []);

  const fetchProductos = async () => {
    try {
      const response = await getAllProducts();
      setProductos(response);
    } catch (error) {
      console.log(error);
    }
  };

  return <TablaProductos productos={productos} />;
};
