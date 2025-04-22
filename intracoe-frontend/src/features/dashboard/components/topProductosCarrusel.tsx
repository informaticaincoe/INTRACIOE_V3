import React, { useState, useEffect } from 'react';
import { Carousel } from 'primereact/carousel';
import { getProductos } from '../services/dashboardServices';

interface Producto {
  producto: number;
  producto__descripcion: string;
  total_vendido: number;
}

export const TopProductosCarousel = () => {
  const [productos, setProductos] = useState<Producto[]>([]);

  useEffect(() => {
    const fetch = async () => {
      const result = await getProductos();
      setProductos(result);
    };
    fetch();
  }, []);

  // Solo mostramos el nombre
  const productoTemplate = (producto: Producto) => {
    return (
      <div className="flex items-center justify-start w-full">
        <p className="text-[1.5vw] font-semibold text-black text-start wrap-break-word">
          {producto.producto__descripcion}
        </p>
      </div>
    );
  };

  return (
    <div className="w-full  overflow-hidden">
      <Carousel
        value={productos}
        numVisible={1}
        numScroll={1}
        autoplayInterval={5000}
        circular
        showIndicators={false}
        showNavigators={false}
        itemTemplate={productoTemplate}
        className="w-full h-full"
      />
    </div>
  );
};
