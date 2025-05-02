import React, { useEffect, useState } from 'react'
import { getAllMovimientosInventario } from '../services/movimientoInventarioServices'
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface'
import { WhiteSectionsPage } from '../../../../shared/containers/whiteSectionsPage'
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'

export const MovimientoInventarioPage = () => {
    const [movimientoList, setMovimientoList] = useState<movimientoInterface[] | undefined>([])
    useEffect(() => {
        fetchMovimientosInventario()
    }, [])

    const fetchMovimientosInventario = async () => {
        try {
            const response = await getAllMovimientosInventario()
            setMovimientoList(response)
        } catch (error) {
            console.log(error)
        }
    }

    return (
        <WhiteSectionsPage>
            <>
                <DataTable value={movimientoList} tableStyle={{ minWidth: '50rem' }}>
                    <Column  
                    header="Tipo"
                    ></Column>
                    <Column field="producto" header="Producto"></Column>
                    <Column field="cantidad" header="Cantidad"></Column>
                    <Column field="fecha" header="Fecha"></Column>
                    <Column field="almacen" header="Almacen"></Column>
                    <Column field="referencia" header="Referencia"></Column>
                </DataTable>
            </>
        </WhiteSectionsPage>
    )
}
