import { useEffect, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { TablaDevolucionesCompra } from '../componentes/tablaDevolucionesCompra'
import { getAllDevolucionesCompra } from '../services/devolucionesCompraServices'

export const DevolucionesCompraPage = () => {
  const [devolucionesCompra, setDevolucionesCompra] = useState<any[]>([])

  useEffect(() => {
    fetchVentas()
  }, [])

  const fetchVentas = async () => {
    try {
      const response = await getAllDevolucionesCompra()
      console.log("VENTAAAAAS", response)
      setDevolucionesCompra(response)
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
          <TablaDevolucionesCompra devolucionesList={devolucionesCompra} />
        </>
      </WhiteSectionsPage>
    </>
  )
}
