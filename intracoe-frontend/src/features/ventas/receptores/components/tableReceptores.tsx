import React, { useRef, useState } from 'react'
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../shared/toast/customToast';
import { useNavigate } from 'react-router';

import { FaCheckCircle } from 'react-icons/fa';
import { IoMdCloseCircle } from 'react-icons/io';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

interface TableReceptoresProps {
    receptores: any
    refreshReceptores: any
}

export const TableReceptores: React.FC<TableReceptoresProps> = ({ receptores, refreshReceptores }) => {
    const [rowClick] = useState<boolean>(true);
    const [selectedProducts, setSelectedProducts] = useState<any[]>([]);
    const toastRef = useRef<CustomToastRef>(null);
    const navigate = useNavigate()

    const handleAccion = (
        severity: ToastSeverity,
        icon: any,
        summary: string
    ) => {
        toastRef.current?.show({
            severity: severity,
            summary: summary,
            icon: icon,
            life: 2000,
        });
    };

    const handleDelete = async () => {
        
    };

    const editHandler = () => {

    };

    return (
        <div>
            {selectedProducts.length > 0 && ( // Verificar si hay productos seleccionados
                <div className="my-5 flex justify-between rounded bg-blue-50 p-5">
                    <p className="text-blue flex items-center gap-2">
                        <FaCheckCircle className="" />
                        receptores seleccionados {selectedProducts.length}
                    </p>
                    <span className="flex gap-2">
                        {selectedProducts.length === 1 && (
                            <span
                                className="border-blue flex items-center gap-2 rounded-md border px-3 py-1 hover:cursor-pointer"
                                onClick={editHandler}
                            >
                                <p className="text-blue">Editar producto</p>
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
            <DataTable
                value={receptores}
                tableStyle={{ minWidth: '50rem' }}
                selectionMode={rowClick ? null : 'multiple'}
                selection={selectedProducts!}
                onSelectionChange={(e: { value: React.SetStateAction<any[]> }) =>
                    setSelectedProducts(e.value)
                }
            >
                <Column
                    selectionMode="multiple"
                    headerStyle={{ width: '3rem' }}
                ></Column>
                <Column field="nombre" header="Nombre" />
                
                <Column field="correo" header="Correo" />
                <Column field="num_documento" header="Documento de identificacion" />
            </DataTable>
            <CustomToast ref={toastRef} />
        </div>
    );
};