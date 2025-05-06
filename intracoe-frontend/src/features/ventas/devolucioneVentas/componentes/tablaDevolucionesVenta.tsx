import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router';
import { ModalDetallesDevolucionesVenta } from './modalDetallesDevolucionesVenta';

interface TablaDevolucionesVentaProps {
  devolucionesList: any[]
}

export const TablaDevolucionesVenta: React.FC<TablaDevolucionesVentaProps> = ({ devolucionesList }) => {
  const [rowClick] = useState<boolean>(true);
  const [selectedDevolucionVenta, setSelectedDevolucionVenta] = useState<any[]>([]);
  const [visibleModal, setVisibleModal] = useState(false)

  const navigate = useNavigate()

  const handleDevolucionSelected = (elemento: any) => {
    console.log(elemento)
    setSelectedDevolucionVenta(elemento)
    setVisibleModal(true)
  }

  useEffect(() => {
    console.log("AAAAAAAAAAAAAAAAAAAA", devolucionesList)
  }, [])

  return (
    <>
      <DataTable
        value={devolucionesList}
        tableStyle={{ minWidth: '50rem' }}
        selectionMode={'single'}
        selection={selectedDevolucionVenta}
        onSelectionChange={(e) =>
          handleDevolucionSelected(e.value)
        }
      >
        <Column field="num_factura" header="Factura"></Column>
        <Column field="fecha" header="Fecha"></Column>
        <Column field="motivo" header="Motivo"></Column>
        <Column field="estado" header="Estado"></Column>
        <Column field="usuario" header="Usuario"></Column>
        <Column header="Acciones"
          body={(rowData: any) => (
            <button className='underline hover:cursor-pointer' onClick={()=>handleDevolucionSelected(rowData)}>Ver detalles</button>
          )}></Column>

      </DataTable>

      {selectedDevolucionVenta && (
        <ModalDetallesDevolucionesVenta
          data={selectedDevolucionVenta} // Solo pasa un ID válido si hay un producto seleccionado
          visible={visibleModal}
          setVisible={setVisibleModal}
        />
      )}
    </>
  )
}
