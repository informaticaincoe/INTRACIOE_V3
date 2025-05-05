import { useEffect, useState } from 'react'
import { getAllMovimientosInventario } from '../services/movimientoInventarioServices'
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Title } from '../../../../shared/text/title'
import { TablaInventarioHeader } from '../componentes/tablaInventarioHeader'
import { Divider } from 'primereact/divider'
import { TablaMovimientoInventario } from '../componentes/tablaMovimientoInventario'
import LoadingScreen from '../../../../shared/loading/loadingScreen'

export const MovimientoInventarioPage = () => {
    const [movimientoList, setMovimientoList] = useState<movimientoInterface[] | undefined>([])
    const [codigoFiltro, setCodigoFiltro] = useState<string>('');
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        fetchMovimientosInventario()
    }, [])

    const fetchMovimientosInventario = async () => {
        try {
            setLoading(true)
            const response = await getAllMovimientosInventario()
            setMovimientoList(response)
        } catch (error) {
            console.log(error)
        }
        finally {
            setLoading(false)
        }
    }

    const handleSearch = (nuevoCodigo: string) => {
        setCodigoFiltro(nuevoCodigo.trim());
    };

    return (
        <>
            {loading && <LoadingScreen/>}
            <Title text={'Movimiento de inventario'} />

            <WhiteSectionsPage>
                <>
                    <TablaInventarioHeader results={movimientoList?.length ?? 0} codigo={codigoFiltro} onSearch={handleSearch} />
                    <Divider />
                    <TablaMovimientoInventario movimientoList={movimientoList} />
                </>
            </WhiteSectionsPage>
        </>
    )
}
