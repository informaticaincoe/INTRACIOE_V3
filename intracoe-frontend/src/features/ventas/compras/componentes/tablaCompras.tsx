import React, { useState } from 'react'
import { useNavigate } from 'react-router';
import { FaCheckCircle } from 'react-icons/fa';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { DeleteModal } from '../../../facturacion/activities/components/modales/deleteModal';
import { CompraInterface } from '../interfaces/comprasInterfaces';
import { deleteComprasById } from '../services/comprasServices';

interface TablaComprasProps {
    comprasList: CompraInterface[] | undefined
    updateList:()=>void
}

export const TablaCompras: React.FC<TablaComprasProps> = ({ comprasList,updateList }) => {
    const [rowClick] = useState<boolean>(true);
    const [selectedCompras, setSelectedCompras] = useState<any[]>([]);
    const [deleteVisible, setDeleteVisible] = useState(false);
    const [itemToDelete, setItemToDelete] = useState<CompraInterface | null>(null);

    const navigate = useNavigate()

    const editHandler = () => {
        console.log(`/compras/${selectedCompras[0].id}`)
        navigate(`/compras/${selectedCompras[0].id}`)
    }

    const handleDelete = () => {
        setItemToDelete(selectedCompras[0]);
        setDeleteVisible(true);
    };


    return (
        <>
            {selectedCompras.length > 0 && ( // Verificar si hay productos seleccionados
                <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
                    <p className="text-blue flex items-center gap-2">
                        <FaCheckCircle className="" />
                        items seleccionados {selectedCompras.length}
                    </p>
                    <span className="flex gap-2">
                        {selectedCompras.length === 1 && (
                            <span
                                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                                onClick={editHandler}
                            >
                                <p className="text-blue">Editar Compras</p>
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
            <DataTable value={comprasList} tableStyle={{ minWidth: '50rem' }} selectionMode={rowClick ? null : 'multiple'}
                selection={selectedCompras!}
                onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                    setSelectedCompras(e.value)
                }
            >
                <Column
                    selectionMode="multiple"
                    headerStyle={{ width: '3rem' }}
                ></Column>
                <Column field="proveedor" header="Proveedor"></Column>
                <Column field="fecha" header="fecha"></Column>
                <Column field="total" header="total"></Column>
                <Column field="estado" header="estado"></Column>    
            </DataTable>
            <DeleteModal
                item={itemToDelete}
                visible={deleteVisible}
                setVisible={setDeleteVisible}
                deleteFunction={(id) => deleteComprasById(String(id))}
                onDeleted={() => {
                    setSelectedCompras([]);
                    updateList()
                }}
            />
        </>
    )
}
