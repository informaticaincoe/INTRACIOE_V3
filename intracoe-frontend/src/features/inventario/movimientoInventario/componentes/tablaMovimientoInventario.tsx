import React, { useEffect, useState } from 'react'
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'
import { FaCaretUp } from 'react-icons/fa6'
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface'
import { ModalDetalleMovimientoInventario } from './modalDetalleMovimientoInventario'

interface TablaMovimientoInventarioProps {
    movimientoList: movimientoInterface[] | undefined
}

export const TablaMovimientoInventario: React.FC<TablaMovimientoInventarioProps> = ({ movimientoList }) => {
    const [visibleModal, setVisibleModal] = useState(false);
    const [selectedProducts, setSelectedProducts] = useState<movimientoInterface | null>(null);
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        setVisibleModal(true)
        if (selectedProducts)
            console.log(selectedProducts)
    }, [selectedProducts])

    return (
        <>
            <DataTable
                value={movimientoList}
                tableStyle={{ minWidth: '50rem' }}
                selectionMode="single"
                selection={selectedProducts} // Se maneja como un único objeto de tipo movimientoInterface
                onSelectionChange={(e) => setSelectedProducts(e.value ? e.value as movimientoInterface : null)}
                dataKey="id"
            >
                <Column
                    header="Tipo"
                    body={(rowData: any) => {
                        return rowData.tipo === "Salida"
                            ?
                            <span className='flex gap-2 text-red'>
                                <FaCaretUp className='rotate-180' />
                                {rowData.tipo}
                            </span>
                            :
                            <span className='flex gap-2 text-green'>
                                <FaCaretUp className=' ' />
                                {rowData.tipo}
                            </span>
                    }}
                ></Column>
                <Column field="nombreProducto" header="Producto"></Column>
                <Column field="cantidad" header="Cantidad"></Column>
                <Column field="fecha" header="Fecha"></Column>
                <Column field="nombreAlmacen" header="Almacen"></Column>
                <Column field="referencia" header="Referencia"></Column>
            </DataTable>

            {selectedProducts && (
                <ModalDetalleMovimientoInventario
                    id={selectedProducts?.id ?? 0} // Solo pasa un ID válido si hay un producto seleccionado
                    visible={visibleModal}
                    setVisible={setVisibleModal}
                />
            )}
        </>
    )
}
