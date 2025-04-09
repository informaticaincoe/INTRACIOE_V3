import { useEffect, useState } from 'react';
import { getAllProducts } from '../../../../shared/services/productos/productosServices';
import { ProductoResponse } from '../../../../shared/interfaces/interfaces';
import { TablaServicios } from './tablaServicios';

interface TablaContainerServiciosProps{
  servicios: ProductoResponse[];
  refreshProducts: () => void;
}

export const TablaContainerServicios:React.FC<TablaContainerServiciosProps> = ({servicios,refreshProducts}) => {
  

  return <TablaServicios servicios={servicios} refreshProducts={refreshProducts} />;
};
