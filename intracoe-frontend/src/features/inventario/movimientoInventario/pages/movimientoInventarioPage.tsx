import { useEffect, useState } from 'react'
import { getAllMovimientosInventario } from '../services/movimientoInventarioServices'
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Title } from '../../../../shared/text/title'
import { TablaInventarioHeader } from '../componentes/tablaInventarioHeader'
import { Divider } from 'primereact/divider'
import { TablaMovimientoInventario } from '../componentes/tablaMovimientoInventario'

export const MovimientoInventarioPage = () => {
    const [movimientoList, setMovimientoList] = useState<movimientoInterface[] | undefined>([])
    const [codigoFiltro, setCodigoFiltro] = useState<string>('');

    useEffect(() => {
        fetchMovimientosInventario()
    }, [])

    const fetchMovimientosInventario = async () => {
        try {
            const response = await getAllMovimientosInventario()
            setMovimientoList(response)
        } catch (error) {
            console.log(error)
        }
    }

    const handleSearch = (nuevoCodigo: string) => {
        setCodigoFiltro(nuevoCodigo.trim());
    };

    return (
        <>
            <Title text={'Movimiento de inventario'} />

            <WhiteSectionsPage>
                <>
                    <TablaInventarioHeader codigo={codigoFiltro} onSearch={handleSearch}/>
                    <Divider />
                    <TablaMovimientoInventario movimientoList={movimientoList}/>
                </>
            </WhiteSectionsPage>
        </>
    )
}
