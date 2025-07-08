import { WhiteCard } from '../whiteCard';
import { Carousel } from 'primereact/carousel';
import { useEffect, useState } from 'react';
import { getProductos } from '../../services/dashboardServices';
import { IoMdOpen } from 'react-icons/io';
import { Dialog } from 'primereact/dialog';
import { FaCrown } from 'react-icons/fa6';

interface Producto {
  producto: number;
  producto__descripcion: string;
  total_vendido: number;
  total_ventas: number;
}

export const ProductosMasVendidosCard = () => {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [productsModalInfo, setProductsModalInfo] = useState<boolean>(false);

  useEffect(() => {
    const fetch = async () => {
      const result = await getProductos();
      console.log("result productos", result);
      setProductos(result);
    };
    fetch();
  }, []);

  const colors= [ // colores para los iconos de corona
    '#FFD700',
    '#c0c0c0',
    '#CD7F32'
  ]

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
            header={
              <div className='px-5 pt-2'>
                <h1>Top 3 productos</h1>
                <p className='font-normal text-lg text-gray'>Detalles de venta</p>
              </div>}
            visible={productsModalInfo}
            style={{ width: '50vw' }}
            onHide={() => {
              if (!productsModalInfo) return;
              setProductsModalInfo(false);
            }}
          >
            <div className='pb-5 px-5'>
              <table className="table-auto w-full text-left">
                <thead>
                  <tr className="border-y border-gray bg-gray-100">
                    <th className="px-4 py-3 text-lg">Producto</th>
                    <th className="px-4 py-3 text-lg">Unidades Vendidas</th>
                    <th className="px-4 py-3 text-lg">Ventas Totales</th>
                  </tr>
                </thead>
                <tbody>
                  {productos.map((producto, index) => (
                    <tr key={index} className="border-b border-gray-400">
                      <td className="px-4 py-3 flex gap-2 items-center"><FaCrown size={20} color={colors[index]}/> {producto.producto__descripcion}</td>
                      <td className="px-4 py-3">{producto.total_vendido}</td>
                      <td className="px-4 py-3">{`$ ${producto.total_ventas.toFixed(2)}`}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Dialog>
        </div>
      )}
    </>
  );
};
