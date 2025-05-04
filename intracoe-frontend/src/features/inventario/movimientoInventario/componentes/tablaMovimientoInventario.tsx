import React, { useState } from 'react'
import { DataTable } from 'primereact/datatable'
import { Column } from 'primereact/column'
import { FaCaretUp } from 'react-icons/fa6'
import { movimientoInterface } from '../interfaces/movimientoInvetarioInterface'
import { FaCheckCircle } from 'react-icons/fa'
import { useNavigate } from 'react-router'
import { deleteMovimientosInventarioById } from '../services/movimientoInventarioServices'

interface TablaMovimientoInventarioProps {
    movimientoList: movimientoInterface[] | undefined
}

export const TablaMovimientoInventario: React.FC<TablaMovimientoInventarioProps> = ({ movimientoList }) => {
    const [rowClick] = useState<boolean>(true);
    const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
    const navigate = useNavigate()

    const editHandler = () => {
        navigate(`/movimiento-inventario/${selectedProducts[0].id}`)  
    }
    
    const handleDelete = async ()=>{
        await deleteMovimientosInventarioById(selectedProducts[0].id)
    }

    return (
        <>
            {selectedProducts.length > 0 && ( // Verificar si hay productos seleccionados
                <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
                    <p className="text-blue flex items-center gap-2">
                        <FaCheckCircle className="" />
                        items seleccionados {selectedProducts.length}
                    </p>
                    <span className="flex gap-2">
                        {selectedProducts.length === 1 && (
                            <span
                                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                                onClick={editHandler}
                            >
                                <p className="text-blue">Editar movimiento</p>
                            </span>
                        )}
                        {
                            <button
                                className="border-red flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                                onClick={handleDelete}
                            >
                                <p className="text-red">Eliminar</p>
                            </button>
                        }
                    </span>
                </div>
            )}
            <DataTable value={movimientoList} tableStyle={{ minWidth: '50rem' }} selectionMode={rowClick ? null : 'multiple'}
                selection={selectedProducts!}
                onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                    setSelectedProducts(e.value)
                }
            >
                <Column
                    selectionMode="multiple"
                    headerStyle={{ width: '3rem' }}
                ></Column>
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
        </>
    )
}
