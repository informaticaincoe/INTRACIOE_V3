import { useEffect, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { getAllDevolucionesVentas } from '../services/devolucionVentaServices'
import { TablaDevolucionesVenta } from '../componentes/tablaDevolucionesVenta'

export const DevoluacionesVentaPage = () => {
    const [devolucionesVenta, setDevolucionesVenta] = useState<any[]>([])

    useEffect(() => {
        fetchVentas()
        fetchDetallesDevolucionesVentas()
    }, [])

    const fetchVentas = async () => {
        try {
            const response = await getAllDevolucionesVentas()
            console.log("VENTAAAAAS", response)
            setDevolucionesVenta(response)
        } catch (error) {
            console.log(error)
        }
    }

    const fetchDetallesDevolucionesVentas = async () => {
        try {
            const response = await getAllDevolucionesVentas()
            console.log("DETALLES DEVOLUCION", response)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <>
            <Title text={'Devoluciones de ventas'} />

            <WhiteSectionsPage>
                <>
                    {/* <TablaComprasHeader codigo={codigoFiltro} onSearch={handleSearch} />
                    <Divider /> */}
                    <TablaDevolucionesVenta devolucionesList={devolucionesVenta} />
                </>
            </WhiteSectionsPage>
        </>
    )
}
