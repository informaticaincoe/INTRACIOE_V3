
import { useEffect, useState } from 'react'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { Title } from '../../../../shared/text/title'
import { Divider } from 'primereact/divider'
import { TableReceptores } from '../components/tableReceptores'
import { getAllReceptor } from '../../../../shared/services/receptor/receptorServices'
import { ReceptorInterface } from '../../../../shared/interfaces/interfaces'
import { HeaderReceptoresOptions } from '../components/headerReceptoresOptions'

export const ReceptoresPage = () => {
  const [receptores, setReceptores] = useState<ReceptorInterface[]>([])
  const [codigoFiltro, setCodigoFiltro] = useState<string>('');

  // Cada vez que cambie el filtro, recargamos los productos
  useEffect(() => {
    fetchReceptores();
  }, [codigoFiltro]);

  const fetchReceptores = async () => {
    try {
      const response = await getAllReceptor()
      console.log(response)
      setReceptores(response)
    } catch (error) {
      console.log(error)
    }
  }

  const handleSearch = (nuevoCodigo: string) => {
    setCodigoFiltro(nuevoCodigo.trim());
  };

  return (
    <>
      <Title text="Receptores" />
      <WhiteSectionsPage>
        <div>
          <HeaderReceptoresOptions codigo={codigoFiltro} onSearch={handleSearch} />
          <Divider />
          <TableReceptores receptores={receptores} refreshReceptores={fetchReceptores} />
        </div>
      </WhiteSectionsPage>
    </>
  )
}
