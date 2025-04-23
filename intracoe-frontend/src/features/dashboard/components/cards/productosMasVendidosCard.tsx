import { WhiteCard } from '../whiteCard'
import { PiTag } from 'react-icons/pi'
import { Carousel } from 'primereact/carousel'
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
    const [productsModalInfo, setProductsModalInfo] = useState<boolean>(false)

    useEffect(() => {
        const fetch = async () => {
            const result = await getProductos();
            console.log(result)
            setProductos(result);
        };
        fetch();
    }, []);

    // Solo mostramos el nombre
    const productoTemplate = (producto: Producto) => {
        return (
            <div className="flex items-center justify-start w-full">
                <p className="text-[1.5vw] font-semibold text-black text-start break-words">
                    {producto.producto__descripcion}
                </p>
            </div>
        );
    };


    return (
        <>
            <WhiteCard>
                <div className=" relative flex justify-between">
                    <span className="flex flex-col gap-2 text-start items w-5/6">
                        <h1 className="font opacity-70">Top 3 productos con mas ventas</h1>
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
                                onPageChange={(e) => setActiveIndex(e.page)}
                            />
                        </div>
                    </span>
                    <span className="bg-secondary-yellow-light text-primary-yellow flex size-10 items-center justify-center rounded-md font-bold text-primary-yellow-dark">
                        {activeIndex + 1}
                    </span>

                    <button className='absolute end-0 bottom-0 opacity-50 hover:cursor-pointer hover:opacity-100' onClick={() => setProductsModalInfo(!productsModalInfo)}>
                        <IoMdOpen size={24} />
                    </button>
                </div>
            </WhiteCard>

            {
                productsModalInfo &&
                <div>
                    <Dialog header="Header" visible={productsModalInfo} style={{ width: '50vw' }} onHide={() => { if (!productsModalInfo) return; setProductsModalInfo(false); }}>
                        <p className="m-0">
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                            consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                        </p>
                    </Dialog>
                </div>
            }
        </>
    )
}