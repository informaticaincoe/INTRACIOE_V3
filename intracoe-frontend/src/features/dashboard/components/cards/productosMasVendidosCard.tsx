import { WhiteCard } from '../whiteCard'
import { TopProductosCarousel } from '../topProductosCarrusel'
import { PiTag } from 'react-icons/pi'

export const ProductosMasVendidosCard = () => {
    return (
        <WhiteCard>
            <div className="flex justify-between">
                <span className="flex flex-col gap-2 text-start items w-5/6">
                    <h1 className="font opacity-70">Top 3 productos con mas ventas</h1>
                    <TopProductosCarousel />
                </span>
                <span className="bg-secondary-yellow-light flex size-10 items-center justify-center rounded-md">
                    <PiTag size={24} color={'#FCC587'} />
                </span>
            </div>
        </WhiteCard>
    )
}