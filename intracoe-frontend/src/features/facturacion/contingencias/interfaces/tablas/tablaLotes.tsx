import { Accordion, AccordionTab } from 'primereact/accordion'
import { Badge } from 'primereact/badge'
import { Column } from 'primereact/column'
import { DataTable } from 'primereact/datatable'
import { FaCheck } from 'react-icons/fa6'
import { FcCancel } from 'react-icons/fc'
import styles from "../../style/ContingenciasTable.module.css"
import React, { useEffect } from 'react'

interface TablaLotesProps {
    lotes: Array<{
        facturas: any[];
    }>
}

export const TablaLotes: React.FC<TablaLotesProps> = ({ lotes }) => {

    useEffect(() => {
        console.log("66666666666666666666", lotes)
    }, [lotes])

    // Helper to render a value or a hyphen if empty
    const renderValue = (value: any) =>
        value !== null && value !== undefined && value !== '' ? value : '-'

    return (
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
                        </DataTable>
                    </AccordionTab>
                )
            })}
        </Accordion>
    )
}
