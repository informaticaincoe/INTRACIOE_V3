import { WhiteCard } from '../whiteCard';
import { PiTag } from 'react-icons/pi';
import { Carousel } from 'primereact/carousel';
import { useEffect, useState } from 'react';
import { getProductos } from '../../services/dashboardServices';
import { IoMdOpen } from 'react-icons/io';
import { Dialog } from 'primereact/dialog';

interface Producto {
  producto: number;
  producto__descripcion: string;
  total_vendido: number;
}

export const ProductosMasVendidosCard = () => {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [productsModalInfo, setProductsModalInfo] = useState<boolean>(false);

  useEffect(() => {
    const fetch = async () => {
      const result = await getProductos();
      console.log(result);
      setProductos(result);
    };
    fetch();
  }, []);

  // Solo mostramos el nombre
  const productoTemplate = (producto: Producto) => {
    return (
      <div className="flex w-full items-center justify-start">
        <p className="text-start text-[1.5vw] font-semibold break-words text-black">
          {producto.producto__descripcion}
        </p>
      </div>
    );
  };

  return (
    <>
      <WhiteCard>
        <div className="relative flex justify-between">
          <span className="items flex w-5/6 flex-col gap-2 text-start">
            <h1 className="font opacity-70">Top 3 productos con mas ventas</h1>
            <div className="w-full overflow-hidden">
              <Carousel
                value={productos}
                numVisible={1}
                numScroll={1}
                autoplayInterval={5000}
                circular
                showIndicators={false}
                showNavigators={false}
                itemTemplate={productoTemplate}
                className="h-full w-full"
                onPageChange={(e) => setActiveIndex(e.page)}
              />
            </div>
          </span>
          <span className="bg-secondary-yellow-light text-primary-yellow text-primary-yellow-dark flex size-10 items-center justify-center rounded-md font-bold">
            {activeIndex + 1}
          </span>

          <button
            className="absolute end-0 bottom-0 opacity-50 hover:cursor-pointer hover:opacity-100"
            onClick={() => setProductsModalInfo(!productsModalInfo)}
          >
            <IoMdOpen size={24} />
          </button>
        </div>
      </WhiteCard>

      {productsModalInfo && (
        <div>
          <Dialog
            header="Header"
            visible={productsModalInfo}
            style={{ width: '50vw' }}
            onHide={() => {
              if (!productsModalInfo) return;
              setProductsModalInfo(false);
            }}
          ></Dialog>
        </div>
      )}
    </>
  );
};
