import React, { useEffect, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'primereact/divider'
import { CompraInterface } from '../interfaces/comprasInterfaces'
import { TablaComprasHeader } from '../componentes/tablaComprasHeader'
import { TablaCompras } from '../componentes/tablaCompras'
import { getAllCompras } from '../services/comprasServices'

export const ComprasPage = () => {
  const [comprasList, setComprasList] = useState<CompraInterface[] | undefined>([])
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  useEffect(() => {
    fetchCompras()
  }, [])

  const fetchCompras = async () => {
    try {
      const response = await getAllCompras()
      setComprasList(response)
    } catch (error) {
      console.log(error)
    }
  }

  const updateList = () => {
    fetchCompras()
  }
  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };
  return (
    <>
      <Title text={'Compras'} />

      <WhiteSectionsPage>
        <>
          <TablaComprasHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaCompras comprasList={comprasList} updateList={updateList}/>
        </>
      </WhiteSectionsPage>
    </>
  )
}
