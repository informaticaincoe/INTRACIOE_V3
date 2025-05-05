import React, { useEffect, useState } from 'react'
import { AjusteInventarioInterface } from '../interfaces/ajusteInventarioInterfaces';
import { getAllAjusteInventario } from '../services/ajusteInventarioServices';
import { Title } from '../../../../shared/text/title';
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage';
import { Divider } from 'antd';
import { TablaAjusteInventario } from '../componentes/tablaAjusteInventario';
import { TablaInventarioHeader } from '../componentes/tablaAjusteInventarioHeader';

export const AjusteInventarioPage = () => {
  const [ajusteInventario, setAjusteInventario] = useState<AjusteInventarioInterface[] | undefined>([])
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  useEffect(() => {
    fetchAjusteInventario()
  }, [])

  const fetchAjusteInventario = async () => {
    try {
      const response = await getAllAjusteInventario()
      setAjusteInventario(response)
    } catch (error) {
      console.log(error)
    }
  }

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Title text={'Ajuste de moivimiento de inventario'} />

      <WhiteSectionsPage>
        <>
          <TablaInventarioHeader results={ajusteInventario?.length ?? 0} codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TablaAjusteInventario ajusteInventario={ajusteInventario} />
        </>
      </WhiteSectionsPage>
    </>
  )
}
