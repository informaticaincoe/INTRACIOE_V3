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
    }, [])

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
                            <Column field="sello_recepcion" header="Sello recepción" />
                            <Column field="fecha_emision" header="Fecha Emisión" />
                            <Column field="total_pagar" header="Total a Pagar" />
                            <Column field="total_iva" header="IVA" />
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