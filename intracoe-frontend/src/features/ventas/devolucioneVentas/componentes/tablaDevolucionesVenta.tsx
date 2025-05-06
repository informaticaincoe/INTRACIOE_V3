import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import React, { useState } from 'react'
import { useNavigate } from 'react-router';

interface TablaDevolucionesVentaProps {
  devolucionesList:any[]
  updateList: any
}

export const TablaDevolucionesVenta:React.FC<TablaDevolucionesVentaProps> = ({devolucionesList, updateList}) => {
  const [rowClick] = useState<boolean>(true);
  const [selectedProveedores, setSelectedProveedores] = useState<any[]>([]);

  const navigate = useNavigate()



  return (
      <>
        
          <DataTable value={devolucionesList} tableStyle={{ minWidth: '50rem' }} selectionMode={rowClick ? null : 'multiple'}
              selection={selectedProveedores!}
              onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                  setSelectedProveedores(e.value)
              }
          >
              <Column
                  selectionMode="multiple"
                  headerStyle={{ width: '3rem' }}
              ></Column>
              <Column field="num_factura" header="Factura"></Column>
              <Column field="fecha" header="Fecha"></Column>
              <Column field="motivo" header="Motivo"></Column>
              <Column field="estado" header="Estado"></Column>
              <Column field="usuario" header="Usuario"></Column>
          </DataTable>
      </>
  )
}
