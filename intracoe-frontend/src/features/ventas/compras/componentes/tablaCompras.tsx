import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router';
import { FaCheckCircle } from 'react-icons/fa';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { DeleteModal } from '../../../facturacion/activities/components/modales/deleteModal';
import { CompraInterface } from '../interfaces/comprasInterfaces';
import { deleteComprasById } from '../services/comprasServices';
import { IoIosWarning } from "react-icons/io";
import { MdCancel } from 'react-icons/md';
import { FaCircleCheck } from 'react-icons/fa6';
import { ModalDetallesCompra } from './modalDetallesCompra';

interface TablaComprasProps {
    comprasList: CompraInterface[] | undefined
    updateList: () => void
}

export const TablaCompras: React.FC<TablaComprasProps> = ({ comprasList, updateList }) => {
    const [selectedCompras, setSelectedCompras] = useState<CompraInterface | undefined>();
    const [visibleModal, setVisibleModal] = useState(false);

    useEffect(() => {
        setVisibleModal(true)
        if (selectedCompras)
            console.log(selectedCompras)
    }, [selectedCompras])

    return (
        <>
            <DataTable
                value={comprasList}
                tableStyle={{ minWidth: '50rem' }}
                selectionMode={'single'}
                selection={selectedCompras}
                onSelectionChange={(e) =>
                    setSelectedCompras(e.value as CompraInterface)
                }
            >
                <Column field="nombreProveedor" header="Proveedor"></Column>
                <Column field="fecha" header="fecha"></Column>
                <Column header="Total"
                    body={(rowData: any) => (
                        <p>$ {rowData.total}</p>
                    )}
                />
                <Column header="Estado"
                    body={(rowData: any) => {
                        if (rowData.estado === "Pendiente") {
                            return (
                                <span className='flex gap-2 text-primary-yellow'>
                                    <IoIosWarning size={24} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        if (rowData.estado === "Pagado") {
                            return (
                                <span className='flex gap-2 text-green'>
                                    <FaCircleCheck size={20} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        if (rowData.estado === "Cancelado") {
                            return (
                                <span className='flex gap-2 text-red'>
                                    <MdCancel size={20} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        return null; // in case there's a state that isn't handled
                    }}
                />
            </DataTable>
            {selectedCompras && (
                <ModalDetallesCompra
                    data={selectedCompras} // Solo pasa un ID válido si hay un producto seleccionado
                    visible={visibleModal}
                    setVisible={setVisibleModal}
                />
            )}
        </>
    )
}
