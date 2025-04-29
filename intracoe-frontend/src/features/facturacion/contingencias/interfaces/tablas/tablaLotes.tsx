import { Accordion, AccordionTab } from 'primereact/accordion'
import { Badge } from 'primereact/badge'
import { Column } from 'primereact/column'
import { DataTable } from 'primereact/datatable'
import { FaCheck, FaCircleCheck } from 'react-icons/fa6'
import { FcCancel } from 'react-icons/fc'
import styles from "../../style/ContingenciasTable.module.css"
import React, { useEffect, useRef } from 'react'
import { enviarFacturaContingencia } from '../../services/contingenciaService.'
import CustomToast, { CustomToastRef, ToastSeverity } from '../../../../../shared/toast/customToast'
import { IoMdCloseCircle } from 'react-icons/io'

interface TablaLotesProps {
    lotes: Array<{
        facturas: any[];
    }>
    contingenciaEstado: any
    updateContingencias: () => void
}

export const TablaLotes: React.FC<TablaLotesProps> = ({ lotes, contingenciaEstado, updateContingencias }) => {
    const toastRef = useRef<CustomToastRef>(null);


    useEffect(() => {
        console.log("66666666666666666666", lotes)
    }, [lotes])

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

    // Helper to render a value or a hyphen if empty
    const renderValue = (value: any) =>
        value !== null && value !== undefined && value !== '' ? value : '-'

    const handleEnviarLote = async (id: number) => {
        try {
            await enviarFacturaContingencia(id)
            handleAccion('success', <FaCircleCheck size={32} />, 'Factura enviada con exito');
            updateContingencias()
        } catch (error) {
            handleAccion('error', <IoMdCloseCircle size={32} />, 'Error al enviar la factura');
        }
    }

    return (
        <>
            <CustomToast ref={toastRef} />

            <Accordion multiple activeIndex={[0]} className={styles.customCollapse}>
                {lotes.map((grupo, id) => {
                    // 1) Todas facturas true
                    const todasTrue = grupo.facturas.every(f => f.recibido_mh === true)
                    // 2) Todas facturas false
                    const todasFalse = grupo.facturas.every(f => f.recibido_mh === false)
                    // 3) Facturas false y true
                    const severity = todasTrue
                        ? 'success'
                        : todasFalse
                            ? 'danger'
                            : 'warning';

                    return (
                        <AccordionTab
                            key={id}
                            header={
                                <div className="flex w-full items-center justify-between gap-2">
                                    <span className="font-bold">Lote {id + 1}</span>
                                    <Badge
                                        value={String(grupo.facturas.length)}
                                        severity={severity}
                                    />
                                </div>
                            }
                        >
                            <DataTable
                                value={grupo.facturas}
                                className={styles.customSubTable}
                            >
                                <Column
                                    header="Numero control"
                                    body={(row: any) => renderValue(row.numero_control)}
                                />
                                <Column
                                    header="Sello recepción"
                                    body={(row: any) => renderValue(row.sello_recepcion)}
                                />
                                <Column
                                    header="Fecha Emisión"
                                    body={(row: any) => renderValue(row.fecha_emision)}
                                />
                                <Column
                                    header="Total a Pagar"
                                    body={(row: any) => renderValue(row.total_pagar)}
                                />
                                <Column
                                    header="IVA"
                                    body={(row: any) => renderValue(row.total_iva)}
                                />
                                <Column
                                    header="Estado"
                                    body={(row: any) =>
                                        row.recibido_mh ? (
                                            <FaCheck className="text-green" />
                                        ) : (
                                            <FcCancel />
                                        )
                                    }
                                />
                                <Column
                                    header="Enviar Lote"
                                    body={(row: any) => {
                                        if (!contingenciaEstado) return

                                        return row.recibido_mh
                                            ? <FaCheck className="text-green" />
                                            : <button className='text-primary-blue border border-primary-blue rounded-md px-2 py-1' onClick={() => handleEnviarLote(row.id)}>
                                                Enviar factura
                                            </button>
                                    }}
                                />
                            </DataTable>
                        </AccordionTab>
                    )
                })}
            </Accordion>
        </>
    )
}
