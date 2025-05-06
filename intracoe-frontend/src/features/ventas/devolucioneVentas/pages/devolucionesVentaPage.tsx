import React, { useEffect, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { getAllDevolucionesVentas } from '../services/devolucionVentaServices'
import { TablaDevolucionesVenta } from '../componentes/tablaDevolucionesVenta'

export const DevoluacionesVentaPage = () => {
    const [devolucionesVenta, setDevolucionesVenta] = useState<any[]>([])

    useEffect(() => {
        fetchVentas()
    }, [])

    const fetchVentas = async () => {
        try {
            const response = await getAllDevolucionesVentas()
            setDevolucionesVenta(response)
        } catch (error) {
            console.log(error)
        }
    }

    const updateList = () => {
        fetchVentas()
    }

    return (
        <>
            <Title text={'Compras'} />

            <WhiteSectionsPage>
                <>
                    {/* <TablaComprasHeader codigo={codigoFiltro} onSearch={handleSearch} />
                 <Divider /> */}
                    <TablaDevolucionesVenta devolucionesList={devolucionesVenta} updateList={updateList} />
                </>
            </WhiteSectionsPage>
        </>
    )
}
