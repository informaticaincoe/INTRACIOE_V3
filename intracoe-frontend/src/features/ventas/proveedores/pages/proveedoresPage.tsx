import React, { useEffect, useState } from 'react'
import { Title } from '../../../../shared/text/title'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Divider } from 'primereact/divider'
import { TablaProveedores } from '../componentes/tablaProveedores'
import { ProveedorInterface } from '../interfaces/proveedoresInterfaces'
import { getAllProveedores } from '../services/proveedoresServices'
import { TablaProveedoresHeader } from '../componentes/tablaProveedoresHeader'

export const ProveedoresPage = () => {
  const [movimientoList, setMovimientoList] = useState<ProveedorInterface[] | undefined>([])
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  useEffect(() => {
    fetchProveedores()
  }, [])

  const fetchProveedores = async () => {
    try {
      const response = await getAllProveedores()
      setMovimientoList(response)
    } catch (error) {
      console.log(error)
    }
  }

  const updateList = () => {
    fetchProveedores()
  }
  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };
  return (
    <>
      <Title text={'Proveedores'} />

      <WhiteSectionsPage>
        <>
          <TablaProveedoresHeader codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaProveedores proveedoresList={movimientoList} updateList={updateList}/>
        </>
      </WhiteSectionsPage>
    </>
  )
}
