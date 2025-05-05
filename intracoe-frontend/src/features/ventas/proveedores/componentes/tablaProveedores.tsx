import React, { useState } from 'react'
import { ProveedorInterface } from '../interfaces/proveedoresInterfaces'
import { useNavigate } from 'react-router';
import { FaCheckCircle } from 'react-icons/fa';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { deleteProveedoresById } from '../services/proveedoresServices';
import { DeleteModal } from '../../../facturacion/activities/components/modales/deleteModal';

interface TablaProveedoresProps {
    proveedoresList: ProveedorInterface[] | undefined
    updateList:()=>void
}

export const TablaProveedores: React.FC<TablaProveedoresProps> = ({ proveedoresList,updateList }) => {
    const [rowClick] = useState<boolean>(true);
    const [selectedProveedores, setSelectedProveedores] = useState<any[]>([]);
    const [deleteVisible, setDeleteVisible] = useState(false);
    const [itemToDelete, setItemToDelete] = useState<ProveedorInterface | null>(null);

    const navigate = useNavigate()

    const editHandler = () => {
        console.log(`/proveedor/${selectedProveedores[0].id}`)
        navigate(`/proveedor/${selectedProveedores[0].id}`)
    }

    const handleDelete = () => {
        setItemToDelete(selectedProveedores[0]);
        setDeleteVisible(true);
    };


    return (
        <>
            {selectedProveedores.length > 0 && ( // Verificar si hay productos seleccionados
                <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
                    <p className="text-blue flex items-center gap-2">
                        <FaCheckCircle className="" />
                        items seleccionados {selectedProveedores.length}
                    </p>
                    <span className="flex gap-2">
                        {selectedProveedores.length === 1 && (
                            <span
                                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                                onClick={editHandler}
                            >
                                <p className="text-blue">Editar proveedor</p>
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
            <DataTable value={proveedoresList} tableStyle={{ minWidth: '50rem' }} selectionMode={rowClick ? null : 'multiple'}
                selection={selectedProveedores!}
                onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                    setSelectedProveedores(e.value)
                }
            >
                <Column
                    selectionMode="multiple"
                    headerStyle={{ width: '3rem' }}
                ></Column>
                <Column field="nombre" header="Nombre"></Column>
                <Column field="ruc_nit" header="Nit/ruc"></Column>
                <Column field="contacto" header="Contacto"></Column>
                <Column field="telefono" header="Telefono"></Column>
                <Column field="email" header="Correo"></Column>
                <Column field="direccion" header="Direccion"></Column>
                <Column field="condiciones_pago" header="Condiciones de pago"></Column>
            </DataTable>
            <DeleteModal
                item={itemToDelete}
                visible={deleteVisible}
                setVisible={setDeleteVisible}
                deleteFunction={(id) => deleteProveedoresById(String(id))}
                onDeleted={() => {
                    setSelectedProveedores([]);
                    updateList()
                }}
            />
        </>
    )
}
