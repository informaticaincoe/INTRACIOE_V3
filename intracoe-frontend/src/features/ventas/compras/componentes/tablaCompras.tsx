import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router';
import { FaCheckCircle, FaRegCheckCircle } from 'react-icons/fa';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { DeleteModal } from '../../../facturacion/activities/components/modales/deleteModal';
import { CompraInterface } from '../interfaces/comprasInterfaces';
import { deleteComprasById } from '../services/comprasServices';
import { IoIosCloseCircleOutline, IoIosWarning } from "react-icons/io";
import { MdCancel } from 'react-icons/md';
import { FaCircleCheck, FaRegCircleCheck } from 'react-icons/fa6';
import { ModalDetallesCompra } from './modalDetallesCompra';
import { CiWarning } from 'react-icons/ci';
import { IoWarningOutline } from 'react-icons/io5';
import dayjs from 'dayjs';

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
                <Column
                    header="fecha y hora"
                    body={(rowData: any) => {
                        return(<p>{dayjs(rowData.fecha).format('DD-MM-YYYY HH:mm:ss')}</p>)
                    }}
                />
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
                                    <IoWarningOutline size={20} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        if (rowData.estado === "Pagado") {
                            return (
                                <span className='flex gap-2 text-green'>
                                    <FaRegCircleCheck size={18} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        if (rowData.estado === "Cancelado") {
                            return (
                                <span className='flex gap-2 text-red'>
                                    <IoIosCloseCircleOutline size={20} />
                                    {rowData.estado}
                                </span>
                            );
                        }
                        return null;
                    }}
                />
            </DataTable>
            {selectedCompras && (
                <ModalDetallesCompra
                    data={selectedCompras}
                    visible={visibleModal}
                    setVisible={setVisibleModal}
                />
            )}
        </>
    )
}